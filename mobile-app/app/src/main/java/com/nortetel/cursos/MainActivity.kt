package com.nortetel.cursos

import android.Manifest
import android.annotation.SuppressLint
import android.content.Intent
import android.content.SharedPreferences
import android.content.pm.ActivityInfo
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.view.ViewGroup
import android.view.View
import android.view.WindowManager
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
 * outra do app, manter a página viva ao voltar do segundo plano, vídeo em
 * tela cheia, e recuperar sozinho se o processo que desenha a página cair.
 */
class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var prefs: SharedPreferences
    private lateinit var webView: WebView
    private var filePathCallback: ValueCallback<Array<Uri>>? = null

    // Estado da tela cheia (vídeo do YouTube etc.) — precisa ficar aqui na
    // Activity, e não só dentro do WebChromeClient, porque o botão "voltar"
    // do celular também precisa saber se tem um vídeo em tela cheia pra
    // fechar ele primeiro, em vez de sair da página.
    private var viewTelaCheia: View? = null
    private var callbackTelaCheia: WebChromeClient.CustomViewCallback? = null

    /**
     * O app existe só pra mostrar esse site — então qualquer navegação
     * http/https (o domínio principal, telas de "acordando o app" depois
     * de inatividade, redirecionamentos de login, o que for) fica dentro
     * do próprio WebView, nunca abre em outro app. Só faz sentido sair do
     * WebView pra esquemas que um navegador não sabe abrir de verdade,
     * tipo "whatsapp:", "mailto:" ou "tel:".
     */
    private fun ficaDentroDoWebView(uri: Uri): Boolean {
        val esquema = uri.scheme?.lowercase()
        return esquema == "http" || esquema == "https" || esquema == null
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

        // O "puxar pra atualizar" (SwipeRefreshLayout) confunde com áreas da
        // página que rolam por conta própria dentro do Streamlit: o Android
        // acha que chegou no topo e recarrega a página sem o usuário querer.
        // Mais seguro simplesmente não ter esse gesto do que ter ele errando.
        binding.swipeRefresh.isEnabled = false

        val urlSalva = prefs.getString("ultima_url", null)
        val urlInicial = if (!urlSalva.isNullOrBlank() && ficaDentroDoWebView(Uri.parse(urlSalva))) {
            urlSalva
        } else {
            getString(R.string.app_url)
        }
        webView.loadUrl(urlInicial)

        onBackPressedDispatcher.addCallback(this) {
            when {
                viewTelaCheia != null -> callbackTelaCheia?.onCustomViewHidden()
                webView.canGoBack() -> webView.goBack()
                else -> {
                    isEnabled = false
                    onBackPressedDispatcher.onBackPressed()
                }
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

    /** Deixa a barra de status/navegação do Android escondida, típico de vídeo em tela cheia. */
    @Suppress("DEPRECATION")
    private fun ativarModoImersivo(ativar: Boolean) {
        if (ativar) {
            window.addFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN)
            window.decorView.systemUiVisibility = (
                View.SYSTEM_UI_FLAG_LAYOUT_STABLE
                    or View.SYSTEM_UI_FLAG_LAYOUT_HIDE_NAVIGATION
                    or View.SYSTEM_UI_FLAG_LAYOUT_FULLSCREEN
                    or View.SYSTEM_UI_FLAG_HIDE_NAVIGATION
                    or View.SYSTEM_UI_FLAG_FULLSCREEN
                    or View.SYSTEM_UI_FLAG_IMMERSIVE_STICKY
                )
        } else {
            window.clearFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN)
            window.decorView.systemUiVisibility = View.SYSTEM_UI_FLAG_VISIBLE
        }
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
        // Necessário para o WebView sequer chamar onCreateWindow (abaixo) em
        // links que abririam em nova aba/janela (target="_blank", o botão
        // "Abrir" dos Materiais, window.open() etc.) — sem isso, o clique
        // não faz literalmente nada, sem erro nenhum.
        settings.setSupportMultipleWindows(true)
        settings.javaScriptCanOpenWindowsAutomatically = true

        webView.addJavascriptInterface(WebAppInterface(this), "Android")

        webView.webViewClient = object : WebViewClient() {
            override fun shouldOverrideUrlLoading(view: WebView, request: WebResourceRequest): Boolean {
                val uri = request.url
                if (ficaDentroDoWebView(uri)) {
                    return false // http/https: sempre fica dentro do app, seja qual for o domínio
                }
                if (!request.isForMainFrame) {
                    return true // recurso/iframe interno com esquema estranho: ignora, não abre nada
                }

                // Esquema que não é página web (whatsapp:, mailto:, tel:, intent:, market: etc.),
                // numa navegação de página inteira: aí sim faz sentido abrir no app certo do celular.
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

                if (url != null && ficaDentroDoWebView(Uri.parse(url))) {
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

            // Vídeo em tela cheia (botão de expandir do player do YouTube).
            // O WebView, por padrão, NÃO sabe mostrar isso sozinho — sem
            // implementar onShowCustomView/onHideCustomView, o botão de tela
            // cheia simplesmente não faz nada.
            override fun onShowCustomView(view: View, callback: CustomViewCallback) {
                if (viewTelaCheia != null) {
                    callback.onCustomViewHidden()
                    return
                }
                viewTelaCheia = view
                callbackTelaCheia = callback

                binding.root.visibility = View.GONE
                (window.decorView as ViewGroup).addView(
                    view,
                    ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT)
                )
                ativarModoImersivo(true)
                requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
            }

            override fun onHideCustomView() {
                val view = viewTelaCheia ?: return
                (window.decorView as ViewGroup).removeView(view)
                binding.root.visibility = View.VISIBLE
                ativarModoImersivo(false)
                requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED

                viewTelaCheia = null
                callbackTelaCheia = null
            }

            // Links que abririam em nova aba/janela (target="_blank", como o
            // botão "Abrir" dos Materiais, ou o link do WhatsApp nas
            // Dúvidas) caem aqui em vez de em shouldOverrideUrlLoading — são
            // sempre um recurso EXTERNO à plataforma (ex: uma pasta do
            // Google Drive), diferente da navegação normal de página
            // inteira (essa sim fica dentro do app). O Android exige
            // "entregar" uma WebView de verdade pra essa janela nova — como
            // o app é uma casca só (sem suportar múltiplas janelas de
            // verdade de fato), usamos uma WebView descartável só pra
            // capturar qual URL foi pedida, e mandamos pro app certo do
            // celular (navegador, Google Drive, WhatsApp etc.) em vez de
            // tentar abrir dentro do próprio app.
            override fun onCreateWindow(
                view: WebView,
                isDialog: Boolean,
                isUserGesture: Boolean,
                resultMsg: android.os.Message
            ): Boolean {
                val webViewTemporaria = WebView(this@MainActivity)
                webViewTemporaria.webViewClient = object : WebViewClient() {
                    override fun shouldOverrideUrlLoading(v: WebView, request: WebResourceRequest): Boolean {
                        try {
                            startActivity(Intent(Intent.ACTION_VIEW, request.url))
                        } catch (_: Exception) {
                            // Nenhum app instalado consegue abrir o link — ignora.
                        }
                        return true
                    }
                }
                (resultMsg.obj as WebView.WebViewTransport).webView = webViewTemporaria
                resultMsg.sendToTarget()
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
