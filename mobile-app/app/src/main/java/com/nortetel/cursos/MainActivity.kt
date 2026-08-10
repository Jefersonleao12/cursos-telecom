package com.nortetel.cursos

import android.Manifest
import android.annotation.SuppressLint
import android.content.Intent
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.view.ViewGroup
import android.view.View
import android.webkit.RenderProcessGoneDetail
import android.webkit.ValueCallback
import android.webkit.WebChromeClient
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.activity.addCallback
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import com.nortetel.cursos.databinding.ActivityMainBinding

/**
 * Casca nativa (WebView) que abre a Plataforma de Treinamentos em
 * Telecomunicações publicada no Streamlit Cloud. O app não guarda nenhum
 * dado nem lógica de negócio — tudo acontece no site; aqui só cuidamos de
 * detalhes que o navegador comum resolve sozinho: permitir baixar o
 * certificado (gerado como blob), lembrar a sessão entre uma abertura e
 * outra do app, manter a página viva ao voltar do segundo plano, e
 * recuperar sozinho se o processo que desenha a página cair.
 */
class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var prefs: SharedPreferences
    private lateinit var webView: WebView
    private var filePathCallback: ValueCallback<Array<Uri>>? = null

    private val dominoPermitido = "cursos-telecom.streamlit.app"

    /**
     * Considera "de dentro do app" tanto o domínio do app quanto qualquer
     * outro endereço do próprio Streamlit (ex: telas intermediárias de
     * "acordando o app" que ficam em outro subdomínio do streamlit.app
     * antes de redirecionar de volta) — só o que for de fato externo
     * (WhatsApp, redes sociais etc.) deve sair do WebView.
     */
    private fun ehDominioInterno(uri: Uri): Boolean {
        val host = uri.host ?: return true // about:blank, about:srcdoc etc: deixa o WebView tratar
        return host == dominoPermitido || host.endsWith(".streamlit.app") || host == "streamlit.app"
    }

    // Script injetado em toda página: intercepta cliques em links "blob:"
    // (usados pelo botão "Baixar PDF" do certificado) e manda os bytes em
    // base64 para o Android salvar na pasta Downloads.
    private val scriptInterceptaDownload = """
        (function() {
            if (window.__cursosTelecomDownloadHook) { return; }
            window.__cursosTelecomDownloadHook = true;
            document.addEventListener('click', function(evento) {
                var alvo = evento.target;
                var link = alvo && alvo.closest ? alvo.closest('a') : null;
                if (!link || !link.href || link.href.indexOf('blob:') !== 0) { return; }
                evento.preventDefault();
                fetch(link.href).then(function(resposta) { return resposta.blob(); }).then(function(blob) {
                    var leitor = new FileReader();
                    leitor.onloadend = function() {
                        var base64 = String(leitor.result).split(',')[1];
                        var nome = link.download || 'certificado.pdf';
                        Android.saveBase64File(base64, nome);
                    };
                    leitor.readAsDataURL(blob);
                });
            }, true);
        })();
    """.trimIndent()

    private val seletorArquivo = registerForActivityResult(
        ActivityResultContracts.StartActivityForResult()
    ) { resultado ->
        val dados = if (resultado.resultCode == RESULT_OK) resultado.data else null
        val uris = if (dados?.data != null) arrayOf(dados.data!!) else null
        filePathCallback?.onReceiveValue(uris)
        filePathCallback = null
    }

    private val pedirPermissaoArmazenamento = registerForActivityResult(
        ActivityResultContracts.RequestPermission()
    ) { /* concedida ou não: a tentativa de download seguinte já reflete isso */ }

    @SuppressLint("SetJavaScriptEnabled")
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        prefs = getSharedPreferences("cursos_telecom", MODE_PRIVATE)

        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.Q &&
            ActivityCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE)
            != PackageManager.PERMISSION_GRANTED
        ) {
            pedirPermissaoArmazenamento.launch(Manifest.permission.WRITE_EXTERNAL_STORAGE)
        }

        webView = binding.webView
        configurarWebView(webView)

        binding.swipeRefresh.setOnRefreshListener { webView.reload() }

        val urlSalva = prefs.getString("ultima_url", null)
        val urlInicial = if (!urlSalva.isNullOrBlank() && ehDominioInterno(Uri.parse(urlSalva))) {
            urlSalva
        } else {
            getString(R.string.app_url)
        }
        webView.loadUrl(urlInicial)

        onBackPressedDispatcher.addCallback(this) {
            if (webView.canGoBack()) {
                webView.goBack()
            } else {
                isEnabled = false
                onBackPressedDispatcher.onBackPressed()
            }
        }
    }

    override fun onResume() {
        super.onResume()
        webView.onResume()
        webView.resumeTimers()
    }

    override fun onPause() {
        webView.onPause()
        webView.pauseTimers()
        super.onPause()
    }

    override fun onDestroy() {
        webView.destroy()
        super.onDestroy()
    }

    /**
     * Troca o WebView atual por um novo, no mesmo lugar do layout. Usado
     * quando o processo que desenha a página cai (onRenderProcessGone) —
     * segundo a documentação do Android, o WebView antigo não pode ser
     * reaproveitado depois de um crash desses, senão a tela fica preta.
     */
    private fun recriarWebView(urlParaCarregar: String) {
        val pai = webView.parent as ViewGroup
        val posicao = pai.indexOfChild(webView)
        val layoutParams = webView.layoutParams

        pai.removeView(webView)
        webView.destroy()

        val novoWebView = WebView(this).apply { id = R.id.webView }
        pai.addView(novoWebView, posicao, layoutParams)

        webView = novoWebView
        configurarWebView(webView)
        webView.loadUrl(urlParaCarregar)
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun configurarWebView(webView: WebView) {
        val settings = webView.settings
        settings.javaScriptEnabled = true
        settings.domStorageEnabled = true
        settings.databaseEnabled = true
        settings.cacheMode = WebSettings.LOAD_DEFAULT
        settings.mediaPlaybackRequiresUserGesture = false
        settings.setSupportZoom(false)
        settings.mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW

        webView.addJavascriptInterface(WebAppInterface(this), "Android")

        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean {
                // Só decide sair do app pra navegação de página inteira (não pra
                // recursos/iframes internos, como o componente injetado do PWA).
                if (!request.isForMainFrame) return false

                val uri = request.url
                if (ehDominioInterno(uri)) {
                    return false // deixa o próprio WebView navegar
                }

                // Link de fato externo (ex: WhatsApp, redes sociais): abre no app/navegador padrão.
                try {
                    startActivity(Intent(Intent.ACTION_VIEW, uri))
                } catch (_: Exception) {
                    // Nenhum app instalado consegue abrir o link — ignora.
                }
                return true
            }

            override fun onRenderProcessGone(view: WebView, detail: RenderProcessGoneDetail): Boolean {
                // O processo que desenha a página pode cair (falta de memória, driver
                // de vídeo, etc.) — sem tratar isso, o WebView fica com a tela preta
                // pra sempre. Trocamos por um WebView novo e recarregamos a página.
                val urlAtual = view.url ?: getString(R.string.app_url)
                recriarWebView(urlAtual)
                return true
            }

            override fun onPageStarted(view: WebView, url: String?, favicon: android.graphics.Bitmap?) {
                super.onPageStarted(view, url, favicon)
                binding.progressBar.visibility = View.VISIBLE
            }

            override fun onPageFinished(view: WebView, url: String?) {
                super.onPageFinished(view, url)
                binding.progressBar.visibility = View.GONE
                binding.swipeRefresh.isRefreshing = false
                view.evaluateJavascript(scriptInterceptaDownload, null)

                if (url != null && ehDominioInterno(Uri.parse(url))) {
                    prefs.edit().putString("ultima_url", url).apply()
                }
            }

            override fun onReceivedError(view: WebView, request: WebResourceRequest, error: WebResourceError) {
                super.onReceivedError(view, request, error)
                if (request.isForMainFrame) {
                    binding.progressBar.visibility = View.GONE
                    binding.swipeRefresh.isRefreshing = false
                }
            }
        }

        webView.webChromeClient = object : WebChromeClient() {
            override fun onShowFileChooser(
                webView: WebView,
                callback: ValueCallback<Array<Uri>>,
                params: FileChooserParams
            ): Boolean {
                filePathCallback?.onReceiveValue(null)
                filePathCallback = callback
                try {
                    seletorArquivo.launch(params.createIntent())
                } catch (_: Exception) {
                    filePathCallback = null
                    return false
                }
                return true
            }
        }

        // Downloads "normais" (materiais hospedados no Supabase Storage, com URL de verdade).
        webView.setDownloadListener { url, _, _, _, _ ->
            try {
                startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
            } catch (_: Exception) {
                // sem app pra lidar com o download — ignora.
            }
        }
    }
}
