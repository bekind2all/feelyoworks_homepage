export async function onRequest(context) {
  const url = new URL(context.request.url);

  if (url.hostname === "www.feelyoworks.com") {
    url.hostname = "feelyoworks.com";
    return Response.redirect(url.toString(), 301);
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
