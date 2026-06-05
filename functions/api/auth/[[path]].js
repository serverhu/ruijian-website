/**
 * Decap CMS OAuth for Cloudflare Pages
 *
 * 处理 GitHub OAuth 登录流程
 * 供 Decap CMS 管理后台使用
 */

// GitHub OAuth endpoints
const GITHUB_AUTH_URL = 'https://github.com/login/oauth/authorize'
const GITHUB_TOKEN_URL = 'https://github.com/login/oauth/access_token'

export async function onRequest(context) {
  const { request, env } = context
  const url = new URL(request.url)
  const path = url.pathname

  // ===== CORS 预检 =====
  if (request.method === 'OPTIONS') {
    return new Response(null, {
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
      },
    })
  }

  // ===== 第一步：跳转到 GitHub 授权 =====
  if (path.endsWith('/auth') && (request.method === 'GET' || request.method === 'POST')) {
    const redirectUri = `${url.origin}/api/auth/callback`
    const clientId = env.OAUTH_GITHUB_CLIENT_ID

    if (!clientId) {
      return new Response('Missing OAUTH_GITHUB_CLIENT_ID', { status: 500 })
    }

    const githubAuthUrl = `${GITHUB_AUTH_URL}?client_id=${clientId}&redirect_uri=${redirectUri}&scope=repo&response_type=code`

    return Response.redirect(githubAuthUrl, 302)
  }

  // ===== 第二步：GitHub 回调，换取 access_token =====
  if (path.endsWith('/callback') && request.method === 'GET') {
    const code = url.searchParams.get('code')
    if (!code) {
      return new Response('Missing authorization code', { status: 400 })
    }

    const clientId = env.OAUTH_GITHUB_CLIENT_ID
    const clientSecret = env.OAUTH_GITHUB_CLIENT_SECRET

    if (!clientId || !clientSecret) {
      return new Response('Missing OAuth credentials', { status: 500 })
    }

    // 用 code 换 token
    const tokenResponse = await fetch(GITHUB_TOKEN_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        client_id: clientId,
        client_secret: clientSecret,
        code,
      }),
    })

    const tokenData = await tokenResponse.json()

    if (tokenData.error) {
      return new Response(`OAuth error: ${tokenData.error_description || tokenData.error}`, { status: 400 })
    }

    // 返回给 Decap CMS 的 HTML 页面
    const content = `
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<script>
(function() {
  const data = ${JSON.stringify(tokenData)}
  if (data.access_token) {
    document.cookie = 'github_token=' + data.access_token + '; path=/; max-age=3600'
  }
  if (window.opener) {
    window.opener.postMessage(data, '*')
    window.close()
  } else {
    document.body.innerHTML = '<p>认证成功，请关闭此页面返回后台。</p>'
  }
})()
</script>
</body>
</html>`

    return new Response(content, {
      headers: {
        'Content-Type': 'text/html; charset=utf-8',
      },
    })
  }

  // ===== 未匹配的路径 =====
  return new Response('Not Found', { status: 404 })
}
