package com.nortetel.cursos

import android.app.Activity
import android.content.ContentValues
import android.content.Context
import android.os.Build
import android.os.Environment
import android.provider.MediaStore
import android.util.Base64
import android.widget.Toast
import java.io.File
import java.io.FileOutputStream

/**
 * Ponte entre o JavaScript da página (injetado em MainActivity) e o Android.
 *
 * O certificado em PDF é gerado em memória pelo Streamlit e oferecido pro
 * navegador como um link "blob:" — não é uma URL de servidor de verdade, então
 * o WebView não consegue baixar isso sozinho. A página, ao clicar em "Baixar
 * PDF", lê o blob em JavaScript, converte pra base64 e chama este método.
 */
class WebAppInterface(private val activity: Activity) {

    @android.webkit.JavascriptInterface
    fun saveBase64File(base64Data: String, nomeArquivo: String) {
        activity.runOnUiThread {
            try {
                val bytes = Base64.decode(base64Data, Base64.DEFAULT)
                val nome = if (nomeArquivo.isBlank()) "certificado.pdf" else nomeArquivo
                salvarEmDownloads(activity, bytes, nome)
                Toast.makeText(activity, "Baixado: $nome (pasta Downloads)", Toast.LENGTH_LONG).show()
            } catch (erro: Exception) {
                Toast.makeText(activity, "Não foi possível salvar o arquivo.", Toast.LENGTH_LONG).show()
            }
        }
    }

    private fun salvarEmDownloads(context: Context, bytes: ByteArray, nomeArquivo: String) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            val resolver = context.contentResolver
            val valores = ContentValues().apply {
                put(MediaStore.MediaColumns.DISPLAY_NAME, nomeArquivo)
                put(MediaStore.MediaColumns.MIME_TYPE, "application/pdf")
                put(MediaStore.MediaColumns.RELATIVE_PATH, Environment.DIRECTORY_DOWNLOADS)
            }
            val uri = resolver.insert(MediaStore.Downloads.EXTERNAL_CONTENT_URI, valores)
                ?: throw IllegalStateException("Não foi possível criar o arquivo de destino.")
            resolver.openOutputStream(uri)?.use { it.write(bytes) }
        } else {
            @Suppress("DEPRECATION")
            val pastaDownloads = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
            if (!pastaDownloads.exists()) pastaDownloads.mkdirs()
            val arquivo = File(pastaDownloads, nomeArquivo)
            FileOutputStream(arquivo).use { it.write(bytes) }
        }
    }
}
