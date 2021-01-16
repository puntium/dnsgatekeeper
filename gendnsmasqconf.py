

blacklist = """
    news.google.com
"""

whitelist = """
    google.com
    googleapis.com
    gstatic.com
    googleusercontent.com
    khanacademy.org
    kastatic.org
    kasandbox.org
    gmail.com
    classdojo.com
    apple.com
    apple-dns.net
    icloud.com
    player.vimeo.com
    opendns.com
    scratch.mit.edu
    q.stripe.com
    quizizz.com
    gvt1.com
    gvt2.com
    gvt3.com
    myschoolapp.com
    bootstrapcdn.com
    static.dreambox.com
    static.zdassets.com
    www.amazon.com
    amazonaws.com
    media-amazon.com
    ssl-images-amazon.com
    fls-na.amazon.com
    www.csus.org
    www.heritagechinese.com
    www.jpl.nasa.gov
    www.tinkercad.com
    wikipedia.org
    wikimedia.org
    menloschool.org
    secure.gravatar.com
    akamaized.net
    typekit.net
    vimeocdn.com
    aaplimg.com
    cloudfront.net
    akadns.net
    online-go.com
    expl.ai
    explaineverything.com
    cdnjs.cloudflare.com
    brilliant.org
    www.recaptcha.net
    cdn.ravenjs.com
    edpuzzle.com
    mysteryscience.com
    mysterydoug.com
    flipgrid.com
    imgix.net
    cdn.mxpnl.com
    wistia.net
    letsencrypt.org
    cdn-apple.com
    dreambox.com
    clever.com
    stream.mux.com
    wistia.com
    crt.comodoca.com
    i.ytimg.com
    goodreads.com
    gr-assets.com
    rackcdn.com
    outschool.com
    zoom.us
    dndbeyond.com
    cursecdn.com
    gravatar.com
    dogonews.com
    smore.com
    nytimes.com
    nyt.com
    sites.google.com
    instructure.com
    instructuremedia.com
    images.unsplash.com
    quizlet.com
    menloschool.org
    makecode.com
    bookcreator.com
    canvas-user-content.com
    firebaseio.com
    googlehosted.com
    peardeck.com
    azureedge.net
    s-microsoft.com
    padlet.org
    slack.com
    slack-edge.com
    tinyurl.com
    spotify.com
    slackb.com
    inscloudgate.net
    waysidepublishing.com
    grammarflip.com
    akamaihd.net
    litix.io
    slideshare.net
    soraapp.com
    veracross.com
    svc.overdrive.com
    api.overdrive.com
    cdnwest-xch.media.net
    od-cdn.com
    biglibraryread.com
    menloschool.okta.com
    oktacdn.com
    login.okta.com
    data.pendo.io
    menloschool.matomo.cloud
    menlocoa.org
    padlet.net
    indicative.com
    padlet.pics
    ingest.sentry.io
    certify.alexametrics.com
    kahoot.it
    cdn.amplitude.com
    static.hotjar.com
    cnn.com
    abcnews.go.com
    abcnews.com
    cdn.segment.com
    warnermediacdn.com
    cdn.turner.com
    ixl.com
    edulastic.com
    biblionasium.com
    digitaldialects.com
    brainpop.com
    myfonts.net
    vimeocdn.com
    squarespace-cdn.com
    buzzin.live
    forms.gle
    firebasehostingproxy.page.link
    menloschool.us6.list-manage.com
    schoology.com
    icloud-content.com
    fulfill.contentreserve.com
    tabroom.com
    redirect.viglink.com
    quizlet.live
    codehs.com
    lichess.org
    lichess1.org
    akamaiedge.net
    fontawesome.com
    images.prismic.io
    imgix.net
    map.fastly.net
    phet.colorado.edu
    socialprogress.org
    purpleair.com
    explorelearning.com
    artofproblemsolving.com
"""

servers = ["208.67.222.222", "208.67.220.220"]


def write_conf_file(file_path):
    with open(file_path, "w") as f:
        f.write("""
    interface=eth0      # Use interface wlan0
    listen-address=192.168.11.2   # Specify the address to listen on
    bind-interfaces      # Bind to the interface
    # REMOVE server=8.8.8.8
    domain-needed        # Don't forward short names
    bogus-priv           # Drop the non-routed address spaces.
    #dhcp-range=192.168.220.50,192.168.220.150,12h # IP range and lease time

    # REMOVE server=8.8.8.8

    # NEW ITEMS
    # Don't resolve any DNS, Blacklist all
    no-resolv
    # Log all queries to /var/log/daemon.log - optional but helpful
    log-queries
    log-facility=-

    # Whitelist domains to DNS lookup
    # uses opendns nameservers, substitute your choice
    # google nameservers are 8.8.8.8 and 8.8.4.4
    # opendns nameservers are 208.67.222.222 and 208.67.220.220
    """)

        for bl in blacklist.strip().split():
            f.write("address=/%s/127.0.0.1\n" % (bl))

        for wl in whitelist.strip().split():
            for s in servers:
                f.write("server=/%s/%s\n" % (wl, s))

        f.write("""
    # Needed if using opendns nameservers
    server=/opendns.com/208.67.222.222
    server=/opendns.com/208.67.220.220

    # Direct all other domains to
    address=/#/127.0.0.1
        """)


if __name__ == "__main__":
    write_conf_file("/tmp/aaadnsmasq.conf")