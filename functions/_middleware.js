export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === "www.feelyoworks.com") {
    url.hostname = "feelyoworks.com";
    return Response.redirect(url.toString(), 301);
  }

  // Google Search Console HTML-file verification must answer 200 at the exact
  // .html URL. Cloudflare Pages otherwise 308-redirects *.html to the
  // extensionless path, which can make periodic re-verification fail.
  if (url.pathname === "/google9bc1d9b7c6206944.html") {
    return new Response("google-site-verification: google9bc1d9b7c6206944.html", {
      status: 200,
      headers: { "Content-Type": "text/html; charset=utf-8" },
    });
  }

  if (url.pathname === "/profile.html") {
    url.pathname = "/profile";
    return Response.redirect(url.toString(), 308);
  }

  if (url.pathname === "/insights.html") {
    url.pathname = "/insights";
    return Response.redirect(url.toString(), 308);
  }

  return context.next();
}
