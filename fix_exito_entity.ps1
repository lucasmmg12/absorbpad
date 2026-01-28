$enc = [System.Text.Encoding]::UTF8

Get-ChildItem -Filter *.html | ForEach-Object {
    $path = $_.FullName
    $content = [System.IO.File]::ReadAllText($path, $enc)
    
    # Replace header with HTML entity to ensure display correctness
    # Matches "Casos de Uso y [Any sequence of non-< characters]xito"
    $content = $content -replace 'Casos de Uso y [^<]*?xito', 'Casos de Uso y &Eacute;xito'
    $content = $content -replace 'Casos de Uso y Ã‰xito', 'Casos de Uso y &Eacute;xito'
    
    [System.IO.File]::WriteAllText($path, $content, $enc)
}
