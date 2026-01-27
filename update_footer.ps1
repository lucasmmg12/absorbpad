$enc = [System.Text.Encoding]::UTF8

# Define the standard footer HTML with correct encoding characters embedded or purely ASCII-safe where possible
# Using char codes for non-ASCII to be 100% safe
$iacute = [char]0x00ED
$ia = "tecnolog${iacute}a"
$Li = "L${iacute}deres"
$o_acute = [char]0x00F3
$absorcion = "absorci${o_acute}n"
$e_acute = [char]0x00E9
$energetica = "energ${e_acute}tica"
$copy = [char]0x00A9

$footerHtml = @"
    <footer class="footer section">
        <div class="footer-container container grid">
            <div class="footer-content">
                <a href="index.html" class="logo footer-logo">
                    <img src="public/assets/images.png" alt="Absorb Pad Logo" class="logo-img">
                    <div class="logo-info">
                        <span class="logo-text">ABSORB <span class="highlight">PAD</span></span>
                        <span class="logo-subtext">S.R.L.</span>
                    </div>
                </a>
                <p class="footer-description">$Li en $ia de $absorcion para la industria minera y $energetica argentina.</p>
                <div class="footer-social">
                    <a href="https://www.linkedin.com/company/absorb-pad-s-r-l" target="_blank"
                        class="footer-social-link"><ion-icon name="logo-linkedin"></ion-icon></a>
                    <a href="https://www.instagram.com/absorpadsrl/" target="_blank"
                        class="footer-social-link"><ion-icon name="logo-instagram"></ion-icon></a>
                    <a href="https://www.facebook.com/people/Absorb-Pad/61586939710791/" target="_blank"
                        class="footer-social-link"><ion-icon name="logo-facebook"></ion-icon></a>
                    <a href="https://api.whatsapp.com/send/?phone=5492644115967&text&type=phone_number&app_absent=0"
                        target="_blank" class="footer-social-link"><ion-icon name="logo-whatsapp"></ion-icon></a>
                </div>
            </div>

            <div class="footer-content">
                <h3 class="footer-title">Contacto</h3>
                <ul class="footer-info">
                    <li class="footer-info-item"><ion-icon name="location-outline"></ion-icon> San Luis 657 (E) | San Juan | AR</li>
                    <li class="footer-info-item"><ion-icon name="call-outline"></ion-icon> +54 9 264 411 5967</li>
                    <li class="footer-info-item"><ion-icon name="mail-outline"></ion-icon> mario.ortiz@absorbpad.com</li>
                </ul>
            </div>
        </div>
        <div class="footer-copy container">
            <p>$copy 2026 Absorb Pad S.R.L. <a href="https://www.growlabs.lat" target="_blank" style="color: inherit; font-weight: bold; text-decoration: none;">Desarrollado por GrowLabs</a></p>
        </div>
    </footer>
"@

Get-ChildItem -Filter *.html | ForEach-Object {
    $path = $_.FullName
    Write-Host "Updating Footer in $path"
    
    $content = [System.IO.File]::ReadAllText($path, $enc)
    
    # Regex to capture footer. Note the dot matches newline (Singleline mode).
    # We look for <footer ... </footer>
    # Assuming standard class="footer...
    
    $pattern = '(?s)<footer\s+class=["'']footer.*?</footer>'
    
    if ($content -match $pattern) {
        $content = $content -replace $pattern, $footerHtml
        [System.IO.File]::WriteAllText($path, $content, $enc)
    }
    else {
        Write-Warning "Footer not found in $path"
    }
}
