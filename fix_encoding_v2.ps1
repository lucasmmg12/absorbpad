$enc = [System.Text.Encoding]::UTF8

# Construct search strings programmatically
$o = [char]0x00F3
$sup3 = [char]0x00B3
$plusminus = [char]0x00B1
$copy = [char]0x00A9
$inv_excl = [char]0x00A1
$ord_fem = [char]0x00BA
$soft_hyphen = [char]0x00AD

$o_sup3 = "$o$sup3"
$o_plusminus = "$o$plusminus"
$o_copy = "$o$copy"
$o_inv_excl = "$o$inv_excl"
$o_ord_fem = "$o$ord_fem"
$o_soft_hyphen = "$o$soft_hyphen"

# Replacements
$search_o_sup3 = $o_sup3
$replace_o_sup3 = "$o"

$search_o_plusminus = $o_plusminus
$replace_o_plusminus = [char]0x00F1 # ñ

$search_o_copy = $o_copy
$replace_o_copy = [char]0x00E9 # é

$search_o_inv_excl = $o_inv_excl
$replace_o_inv_excl = [char]0x00E1 # á

$search_o_ord_fem = $o_ord_fem
$replace_o_ord_fem = [char]0x00FA # ú

$search_o_soft_hyphen = $o_soft_hyphen
$replace_o_soft_hyphen = [char]0x00ED # í

Get-ChildItem -Filter *.html | ForEach-Object {
    $path = $_.FullName
    Write-Host "Processing $path"
    
    $content = [System.IO.File]::ReadAllText($path, $enc)
    $originalLength = $content.Length
    
    $content = $content.Replace($search_o_sup3, $replace_o_sup3)
    $content = $content.Replace($search_o_plusminus, $replace_o_plusminus)
    $content = $content.Replace($search_o_copy, $replace_o_copy)
    $content = $content.Replace($search_o_inv_excl, $replace_o_inv_excl)
    $content = $content.Replace($search_o_ord_fem, $replace_o_ord_fem)
    $content = $content.Replace($search_o_soft_hyphen, $replace_o_soft_hyphen)
    
    # Also clean strict 'Lóderes' and 'tecnologóa' if soft hyphen was stripped earlier or differently
    # Lóderes -> Líderes (ó -> í)
    # tecnologóa -> tecnología (ó -> í)
    # But only in these words!
    $content = $content.Replace("L${o}deres", "L$([char]0x00ED)deres")
    $content = $content.Replace("tecnolog${o}a", "tecnolog$([char]0x00ED)a")

    if ($content.Length -ne $originalLength -or $true) {
        [System.IO.File]::WriteAllText($path, $content, $enc)
        Write-Host "Modified $path"
    }
}
