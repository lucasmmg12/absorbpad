$enc = [System.Text.Encoding]::UTF8

Get-ChildItem -Filter *.html | ForEach-Object {
    $path = $_.FullName
    $content = [System.IO.File]::ReadAllText($path, $enc)
    
    # Regex replace to catch whatever garbled characters are between "y" and "xito" or just replace the whole header content
    $content = $content -replace 'Casos de Uso y .*?xito</h2>', 'Casos de Uso y Éxito</h2>'
    # Also handle if it's "Exito" without accent just in case, though we want "Éxito"
    
    [System.IO.File]::WriteAllText($path, $content, $enc)
    Write-Host "Processed $path"
}
