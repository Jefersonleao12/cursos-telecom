package com.nortetel.cursos

import android.Manifest
import android.annotation.SuppressLint
import android.content.Intent
import android.content.SharedPreferences
import android.content.pm.PackageManager
import android.net.Uri
import android.os.Build
import android.os.Bundle
import android.view.View
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
 * outra do app, e navegação/voltar do jeito que se espera de um app.
 */
class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var prefs: SharedPreferences
    private var filePathCallback: ValueCallback<Array<Uri>>? = null

    private val dominoPermitido = "cursos-telecom.streamlit.app"

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

        configurarWebView()

        binding.swipeRefresh.setOnRefreshListener { binding.webView.reload() }

        val urlSalva = prefs.getString("ultima_url", null)
        val urlInicial = if (!urlSalva.isNullOrBlank() && Uri.parse(urlSalva).host == dominoPermitido) {
            urlSalva
        } else {
            getString(R.string.app_url)
        }
        binding.webView.loadUrl(urlInicial)

        onBackPressedDispatcher.addCallback(this) {
            if (binding.webView.canGoBack()) {
                binding.webView.goBack()
            } else {
                isEnabled = false
                onBackPressedDispatcher.onBackPressed()
            }
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun configurarWebView() {
        val webView = binding.webView
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
                val uri = request.url
                return if (uri.host == dominoPermitido) {
                    false // deixa o próprio WebView navegar
                } else {
                    // Link pra fora do app (ex: WhatsApp, redes sociais): abre no app/navegador padrão.
                    try {
                        startActivity(Intent(Intent.ACTION_VIEW, uri))
                    } catch (_: Exception) {
                        // Nenhum app instalado consegue abrir o link — ignora.
                    }
                    true
                }
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

                if (url != null && Uri.parse(url).host == dominoPermitido) {
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
