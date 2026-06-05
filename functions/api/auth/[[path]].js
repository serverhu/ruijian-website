/**
 * Decap CMS OAuth — Cloudflare Pages Function
 *
 * 处理 GitHub OAuth 登录回调
 * 需要 Cloudflare Pages 环境变量：
 *   OAUTH_GITHUB_CLIENT_ID
 *   OAUTH_GITHUB_CLIENT_SECRET
 */
export async function onRequest(context) {
  const { request, env } = context
  const url = new URL(request.url)
  const path = url.pathname

  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
  }

  if (request.method === 'OPTIONS') {
    return new Response(null, { headers })
  }

  const clientId = env.OAUTH_GITHUB_CLIENT_ID
  const clientSecret = env.OAUTH_GITHUB_CLIENT_SECRET

  // ===== 第一步：跳转到 GitHub 授权页面 =====
  if (request.method === 'GET' && path.endsWith('/auth')) {
    const redirectUri = `${url.origin}/api/auth/callback`
    const githubUrl = `https://github.com/login/oauth/authorize?client_id=${clientId}&redirect_uri=${redirectUri}&scope=repo&response_type=code`
    return Response.redirect(githubUrl, 302)
  }

  // ===== 第二步：GitHub 回调，换 token =====
  if (request.method === 'GET' && path.endsWith('/callback')) {
    const code = url.searchParams.get('code')
    if (!code) return new Response('Missing code', { status: 400 })

    const tokenRes = await fetch('https://github.com/login/oauth/access_token', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'application/json' },
      body: JSON.stringify({ client_id: clientId, client_secret: clientSecret, code }),
    })
    const data = await tokenRes.json()

    if (data.error) return new Response(`Error: ${data.error}`, { status: 400 })

    // 返回给 Decap CMS 的关闭窗口页面
    return new Response(
      `<html><body><script>
        window.opener.postMessage(${JSON.stringify(data)}, '*')
        window.close()
      </script></body></html>`,
      { headers: { 'Content-Type': 'text/html; charset=utf-8', ...headers } }
    )
  }

  return new Response('Not Found', { status: 404 })
}
