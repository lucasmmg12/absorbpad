Get-ChildItem -Filter *.html | ForEach-Object {
    $path = $_.FullName
    # Force read as UTF8. If the preamble is missing, it might misinterpret, but usually okay for these files.
    # We use a stream reader to be sure or just strict UTF8.
    $content = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    
    # Fix 'ó' base artifacts
    $content = $content.Replace('ó³', 'ó')
    $content = $content.Replace('ó±', 'ñ')
    $content = $content.Replace('ó©', 'é')
    $content = $content.Replace('ó¡', 'á')
    $content = $content.Replace('óº', 'ú')
    $content = $content.Replace('ó­', 'í')
    
    # Fix 'í' base artifacts (if any remain)
    $content = $content.Replace('í³', 'ó')
    $content = $content.Replace('í±', 'ñ')
    $content = $content.Replace('í©', 'é')
    $content = $content.Replace('í¡', 'á')
    $content = $content.Replace('íº', 'ú')
    $content = $content.Replace('í­', 'í')

    # Specific word fixes
    $content = $content.Replace('Lóderes', 'Líderes')
    $content = $content.Replace('tecnologóa', 'tecnología')
    $content = $content.Replace('metálicas', 'metálicas') 

    # Clean up soft hyphens if they are naked
    $content = $content.Replace('­', '') 

    [System.IO.File]::WriteAllText($path, $content, [System.Text.Encoding]::UTF8)
}
