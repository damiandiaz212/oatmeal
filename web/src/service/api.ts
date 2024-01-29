const base = "";

export async function getPortfolioIds() {
  const resp = await fetch(`${base}/api/ids`, {
    method: "GET",
    mode: "same-origin",
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  });
  return resp.json();
}

export async function getPortfolioStatus(id: string) {
  const resp = await fetch(`${base}/api/status?id=${id}`, {
    method: "GET",
    mode: "same-origin",
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  });
  return resp.json();
}

export async function getTransactions(id: string) {
  const resp = await fetch(`${base}/api/transactions?id=${id}`, {
    method: "GET",
    mode: "same-origin",
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  });
  return resp.json();
}

export async function deletePortfolio(id: string) {
  const resp = await fetch(`${base}/api/delete?id=${id}`, {
    method: "GET",
    mode: "same-origin",
    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  });
  return resp.json();
}
