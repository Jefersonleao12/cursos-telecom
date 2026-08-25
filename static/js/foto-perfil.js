/**
 * Redimensiona e comprime uma foto no navegador ANTES do upload — sem
 * isso, uma foto de celular (às vezes 5-10MB) precisa subir inteira até
 * o servidor numa rede móvel, o que pode levar dezenas de segundos e
 * trava a tela em conexões ruins. Como o servidor recorta a foto pra
 * 400x400 de qualquer jeito (ver database/repositorio.py:
 * _processar_foto_perfil), não faz sentido mandar o arquivo original
 * inteiro — comprimir aqui já resolve o problema na raiz.
 *
 * Retorna um novo File já comprimido (JPEG), ou null se não foi possível
 * comprimir nesse navegador (ex: formato não suportado por
 * createImageBitmap) — nesse caso quem chamou deve usar o arquivo
 * original mesmo, sem travar o envio.
 */
async function comprimirFoto(arquivo, ladoMaximo = 900, qualidade = 0.85) {
    try {
        const bitmap = await createImageBitmap(arquivo);
        let { width, height } = bitmap;
        if (width > ladoMaximo || height > ladoMaximo) {
            if (width > height) {
                height = Math.round((height * ladoMaximo) / width);
                width = ladoMaximo;
            } else {
                width = Math.round((width * ladoMaximo) / height);
                height = ladoMaximo;
            }
        }
        const canvas = document.createElement("canvas");
        canvas.width = width;
        canvas.height = height;
        canvas.getContext("2d").drawImage(bitmap, 0, 0, width, height);
        const blob = await new Promise((resolve) => canvas.toBlob(resolve, "image/jpeg", qualidade));
        if (!blob) return null;
        return new File([blob], "foto.jpg", { type: "image/jpeg" });
    } catch (erro) {
        console.warn("Não foi possível comprimir a foto no navegador, enviando o arquivo original:", erro);
        return null;
    }
}

/**
 * Liga um <input type="file"> ao fluxo de compressão + pré-visualização:
 * ao escolher uma foto, comprime (se possível), substitui o arquivo do
 * próprio input pelo comprimido (assim o <form> normal já envia a versão
 * leve, sem precisar reescrever o envio pra JavaScript/fetch) e chama
 * `aoAtualizarPreview(url)` com a URL de pré-visualização.
 */
function ligarCompressaoDeFoto(inputEl, aoAtualizarPreview) {
    inputEl.addEventListener("change", async () => {
        const arquivo = inputEl.files[0];
        if (!arquivo) {
            aoAtualizarPreview(null);
            return;
        }
        const comprimido = await comprimirFoto(arquivo);
        if (comprimido) {
            const dt = new DataTransfer();
            dt.items.add(comprimido);
            inputEl.files = dt.files;
            aoAtualizarPreview(URL.createObjectURL(comprimido));
        } else {
            aoAtualizarPreview(URL.createObjectURL(arquivo));
        }
    });
}
