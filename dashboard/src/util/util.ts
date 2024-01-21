export function openSampleSite() {
  const path =
    "/html/body/div[3]/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div[2]/div";
  const container = document.evaluate(
    path,
    document,
    null,
    XPathResult.FIRST_ORDERED_NODE_TYPE,
    null
  ).singleNodeValue;
  const frame = document.createElement("iframe");
  if (frame) {
    frame.src = "http://localhost:3000/serve";
    container?.appendChild(frame);
  }
}
