import store from './store.js'

export function getToken(email, password) {
    store.headers.set('Authorization', 'Basic ' + btoa(email + ':' + password));
    return fetch('/api/v1/auth/request-token', {
        method: 'POST',
        headers: store.headers
    })
        .then(response => response.json())
        .then(data => {
            if (data.token) {
                store.isAuthenticated = true;
                store.headers.set('Authorization', 'Bearer ' + data.token);
            }
            return data
        })
}

export function logout() {
    return fetch('/api/v1/auth/logout', {
        headers: store.headers
    }).then(response => {
        store.isAuthenticated = false;
        store.headers.delete('Authorization');
        return response;
    })
}

export function register(data) {
    const result = {'ok': false};
    return fetch('/api/v1/auth/register', {
        method: 'POST',
        headers: store.headers,
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            result.ok = true;
        }
        return response.json()
    }).then(data => {
        result.data = data;
        return result;
    })
}

export function requestPasswordReset(email) {
    return fetch('/api/v1/auth/request-password-reset', {
        method: 'POST',
        headers: store.headers,
        body: JSON.stringify({'email': email})
    }).then(response => response.json())
}

export function resetPassword(data) {
    return fetch('/api/v1/auth/reset-password', {
        method: 'POST',
        headers: store.headers,
        body: JSON.stringify(data)
    }).then(response => response.json())
}

export function getAuthUser() {
    return fetch('/api/v1/users/me', {
        headers: store.headers
    })
        .then(response => response.json())
}

export function getUsers() {
    return fetch('/api/v1/users/', {
        headers: store.headers
    })
        .then(response => response.json())
}

export function putUser(id, data) {
    return fetch(`/api/v1/users/${id}`, {
        headers: store.headers,
        method: 'PUT',
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            return {};
        } else {
            return response.json();
        }
    })
}

export function getBookmarks(queryString='') {
    const result = {};
    return fetch(`/api/v1/bookmarks/${queryString}`, {
        headers: store.headers
    }).then(response => {
        result['pagination'] = JSON.parse(response.headers.get('x-pagination'));
        if (response.ok) {
            return response.json()
        } else {
            return []
        }
    }).then(data => {
        result['bookmarks'] = data;
        return result;
    })
}

export function getBookmark(id) {
    return fetch(`/api/v1/bookmarks/${id}`, {
        headers: store.headers
    }).then(response => response.json())
}

export function postBookmarks(data) {
  return fetch('/api/v1/bookmarks/', {
    headers: store.headers,
    method: 'POST',
    body: JSON.stringify(data)
  }).then(response => {
        if (response.ok) {
            return {'location': response.headers.get('location')}
        } else {
            return response.json()
        }
  })
}

export function suggestTitle(url) {
  return fetch('/api/v1/suggest-title', {
    headers: store.headers,
    method: 'POST',
    body: JSON.stringify({'url': url})
  }).then(response => response.json())
}

export function getTags() { 
    return fetch('/api/v1/tags/', {
        headers: store.headers
    }).then(response => {
        if (response.ok) {
            return response.json()
        } else {
            return []
        }
    })
}

export function getSubscriptions() {
    return fetch('/api/v1/subscriptions/', {
        headers: store.headers
    })
        .then(response => {
            if (response.ok){
                return response.json()
            } else {
                return []
            }
        })
}

export function postSubscription(user_id) {
    let payload = {'user_id': user_id};
    return fetch('/api/v1/subscriptions/', {
        method: 'POST',
        headers: store.headers,
        body: JSON.stringify(payload)
    })
        .then(response => {
            if (response.ok) {
                return {}
            } else {
                return response.json()
            }
        })
}

export function putBookmark(bookmark_id, data) {
    return fetch(`/api/v1/bookmarks/${bookmark_id}`, {
        method: 'PUT',
        headers: store.headers,
        body: JSON.stringify(data)
    }).then(response => {
        if (response.ok) {
            return {};
        }
        return response.json();
    })
}

export function deleteBookmark(id) {
    return fetch(`/api/v1/bookmarks/${id}`, {
        method: 'DELETE',
        headers: store.headers
    })
        .then(response => {
            if (response.ok) {
                return {}
            } else {
                return response.json()
            }
        })

}

export function deleteSubscription(user_id) {
    return fetch(`/api/v1/subscriptions/${user_id}`, {
        method: 'DELETE',
        headers: store.headers
    })
        .then(response => {
            if (response.ok) {
                return {}
            } else {
                return []
            }
        })
}
export function getVote(id) {
    return fetch('/api/v1/votes/' + id, {
        headers: store.headers,
    }).then(response => response.json())
}

export function postVote(bookmark_id, direction) {
    let payload = {'bookmark_id': bookmark_id, 'direction': direction};
    return fetch('/api/v1/votes/', {
        method: 'POST',
        headers: store.headers,
        body: JSON.stringify(payload)
    }).then(response => {
        if (response.ok) {
            return {'location': response.headers.get('location')}
        } else {
            return response.json()
        }
    })
}

export function putVote(vote_id, direction) {
    let payload = {'direction': direction};
    return fetch('/api/v1/votes/' + vote_id, {
        method: 'PUT',
        headers: store.headers,
        body: JSON.stringify(payload)
    }).then(response => {
        if (response.ok) {
            return {};
        } else {
            return response.json()
        }
    })
}

export function deleteVote(vote_id) {
    return fetch('/api/v1/votes/' + vote_id, {
        method: 'DELETE',
        headers: store.headers
    }).then(response => {
        if (response.ok) {
            return {}
        } else {
            return response.json()
        }
    })
}

export function getFavourites() {
    return fetch('/api/v1/favourites/', {
        headers: store.headers
    })
        .then(response => {
            if (response.ok) {
                return response.json()
            } else {
                return []
            }
        })
}

export function postFavourite(bookmark_id) {
    let payload = {'bookmark_id': bookmark_id};
    return fetch('/api/v1/favourites/', {
        method: 'POST',
        headers: store.headers,
        body: JSON.stringify(payload)
    }).then(response => response.json())
}

export function deleteFavourite(favourite_id) {
    return fetch('/api/v1/favourites/' + favourite_id, {
        method: 'DELETE',
        headers: store.headers,
    }).then(response => {
        if (response.ok) {
            return {}
        } else {
            return response.json()
        }
    })
}
