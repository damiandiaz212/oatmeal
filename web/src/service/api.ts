const base = "http://localhost:5000";

export async function getPortfolioIds() {
  const resp = await fetch(`${base}/api/ids`, {
    method: "GET",

    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  });
  return resp.json();
}

export async function getPortfolioStatus(id: string) {
  const resp = await fetch(`${base}/api/status?id=${id}`, {
    method: "GET",

    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  });
  return resp.json();
}

export async function getTransactions(id: string) {
  const resp = await fetch(`${base}/api/transactions?id=${id}`, {
    method: "GET",

    headers: {
      "Content-type": "application/json; charset=UTF-8",
    },
  });
  return resp.json();
}
