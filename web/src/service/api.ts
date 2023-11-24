const baseUrl = ''
export function registerUser (email: string) {
  return fetch(`${baseUrl}`, {
    method: 'POST',
    body: JSON.stringify({
      email,
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    },
  })
}
export function uploadImage (email: string, image: any) {
  return fetch(`${baseUrl}`, {
    method: 'POST',
    body: JSON.stringify({
      email,
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    },
  })
}
export function serveImage (email: string, refImage: any) {
  return fetch(`${baseUrl}`, {
    method: 'POST',
    body: JSON.stringify({
      email,
      refImage,
    }),
    headers: {
      'Content-type': 'application/json; charset=UTF-8',
    },
  })
}
