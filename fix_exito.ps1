$enc = [System.Text.Encoding]::UTF8

# We know specific corruptions now
$bad_Exito_1 = "ó‰xito" 
$bad_Exito_2 = "Ã‰xito" 
$bad_Exito_3 = "Ã©xito" # lowercase

Get-ChildItem -Filter *.html | ForEach-Object {
    $path = $_.FullName
    
    $content = [System.IO.File]::ReadAllText($path, $enc)
    $original = $content
    
    # Check for "ó‰" which is likely "É" corrupted
    $content = $content.Replace("ó‰", "É")
    
    # Fix the specific title phrase to be sure
    $content = $content.Replace("Casos de Uso y ó‰xito", "Casos de Uso y Éxito")
    $content = $content.Replace("Casos de Uso y Éxito", "Casos de Uso y Éxito") # Just ensuring
    $content = $content.Replace("Casos de Uso y Ã‰xito", "Casos de Uso y Éxito")

    if ($content -ne $original) {
        [System.IO.File]::WriteAllText($path, $content, $enc)
        Write-Host "Fixed Éxito in $path"
    }
}
