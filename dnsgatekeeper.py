from aiohttp import web

import asyncio
import sys
import elevate
import time

import gendnsmasqconf

elevate.elevate()

def render():

    fw_state = "unknown"
    if is_blocked:
        fw_state = "Firewall is ON. Traffic is blocked"
    else:
        fw_state = "Firewall is OFF. Traffic is allowed"

    off_for_state = ""
    if secs_until_back_on:
        off_for_state = "Traffic will be blocked again in %.1f minutes" % (secs_until_back_on / 60.0)

    body = """
    <html>
        <head>
            <!-- Required meta tags -->
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

            <link rel="stylesheet" 
                  href="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/css/bootstrap.min.css" 
                  integrity="sha384-TX8t27EcRE3e/ihU7zmQxVncDAy5uIKz4rEkgIXeMed4M0jlfIDPvg6uqKI2xXr2" 
                  crossorigin="anonymous">

            <!-- Option 1: jQuery and Bootstrap Bundle (includes Popper) -->
            <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@4.5.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-ho+j7jyWK8fNQe+A12Hb8AhRq26LrZ/JpcUGGOn+Y7RsweNrtN/tE3MoK7ZeZDyx" crossorigin="anonymous"></script>

        </head>
        <body>
            <div class="container-sm">
                <h1 class="display-3">%s</h1>
                %s
                <form method="post" action="/">
                    <button name="button_on" class="btn btn-danger">BLOCK TRAFFIC</button>
                    <button name="button_off" class="btn btn-success">ALLOW TRAFFIC</button>
                    <div class="list-group mt-3">
                        <button name="button_off_30min" class="list-group-item list-group-item-action">ALLOW for 30 minutes</button>
                        <button name="button_off_60min" class="list-group-item list-group-item-action">ALLOW for 60 minutes</button>
                        <button name="button_off_120min" class="list-group-item list-group-item-action">ALLOW for 2 hours</button>
                    </div>
                </form>
                <a href="/" class="btn btn-info">Refresh</a>
            </div>
        </body>
    </html>
    """ % (
        fw_state,
        off_for_state
    )

    return body

dnsmasq_process = None
is_blocked = None
secs_until_back_on = None
back_on_task = None

async def handle(request):
    #name = request.match_info.get('name', "Anonymous")
    text = "Hello, " + "ken"
    return web.Response(body=render(), content_type="text/html")

async def handle_post(request):
    print("in post handler")
    print(request)
    vals = await request.post()
    if "button_on" in vals:
        await block_on()
    elif "button_off" in vals:
        await block_off()
    elif "button_off_30min" in vals:
        await block_off(30 * 60)
    elif "button_off_60min" in vals:
        await block_off(60 * 60)
    elif "button_off_120min" in vals:
        await block_off(120 * 60)

    return web.Response(body=render(), content_type="text/html")


async def kill_dnsmasq():
    global dnsmasq_process
    if dnsmasq_process is not None:
        print("killing existing dnsmasq...")
        try:
            dnsmasq_process.kill()
            await dnsmasq_process.wait()
        except ProcessLookupError:
            print("got process lookup error")
            pass
        
        dnsmasq_process = None

async def block_on(after_secs=None):
    if after_secs:
        wait_until = time.time() + after_secs
        global secs_until_back_on
        # sleep for 5 seconds at a time until we're done
        while time.time() < wait_until:
            secs_until_back_on = wait_until - time.time()
            print("%s more seconds to wait" % (secs_until_back_on))
            await asyncio.sleep(5)

        secs_until_back_on = None
    else:
        global back_on_task
        global secs_until_back_on
        if back_on_task:
            back_on_task.cancel()
            secs_until_back_on = None
        

    await kill_dnsmasq()
    conf_file_path = "/tmp/bbbdnsmasq.conf"
    print("starting new dnsmasq with blocking config")
    gendnsmasqconf.write_conf_file(conf_file_path)
    global dnsmasq_process
    print("starting process")
    dnsmasq_process = await asyncio.create_subprocess_exec(
        '/usr/sbin/dnsmasq', '-k', '--conf-file=%s' % (conf_file_path),
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    print("return code was", dnsmasq_process.returncode)
    global is_blocked
    is_blocked = True

# dnsmasq -k --log-queries --log-facility=-
async def block_off(on_timer_secs=None):
    await kill_dnsmasq()
    global dnsmasq_process
    dnsmasq_process = await asyncio.create_subprocess_exec(
        '/usr/sbin/dnsmasq', '-k', '--log-queries', '--log-facility=-', 
        stdout=sys.stdout,
        stderr=sys.stderr
    )
    global is_blocked
    is_blocked = False

    global back_on_task
    global secs_until_back_on
    if back_on_task:
        back_on_task.cancel()
        secs_until_back_on = None
        

    if on_timer_secs:
        back_on_task = asyncio.ensure_future(block_on(on_timer_secs))




app = web.Application()
app.router.add_get('/', handle)
app.router.add_post('/', handle_post)
#app.router.add_get('/{name}', handle)

async def on_startup(app):
    await block_on()

app.on_startup.append(on_startup)

web.run_app(app)

