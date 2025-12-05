# 🔐 Guide Complet: Signer Numériquement Flemme

## Pourquoi Signer Votre Application?

### Sans Signature

Quand un utilisateur télécharge `Flemme Setup.exe`, Windows affiche:

```
⚠️ Windows a protégé votre PC
Microsoft Defender SmartScreen a empêché le démarrage d'une application non reconnue.
```

**Impact:**
- ❌ Mauvaise expérience utilisateur
- ❌ Perte de confiance
- ❌ Beaucoup d'utilisateurs abandonnent l'installation
- ❌ Windows peut bloquer le téléchargement

### Avec Signature

```
✅ Éditeur vérifié: Votre Nom/Entreprise
✅ Installation sans avertissement
✅ Confiance immédiate
```

---

## 📋 Options de Signature

### Option 1: Certificat Code Signing Standard (~$200/an)

**Avantages:**
- ✅ Moins cher
- ✅ Validation plus rapide
- ✅ Fichier .pfx facile à utiliser

**Inconvénients:**
- ⚠️ Réputation SmartScreen à construire
- ⚠️ Avertissements possibles pendant ~3 mois
- ⚠️ Nécessite plusieurs milliers d'installations sans incident

**Recommandé pour:** Petits projets, distribution limitée

---

### Option 2: Certificat EV Code Signing (~$400/an) ⭐ RECOMMANDÉ

**Avantages:**
- ✅ **Réputation immédiate** auprès de SmartScreen
- ✅ Aucun avertissement dès la première installation
- ✅ Validation d'identité renforcée (plus de confiance)
- ✅ Peut signer des drivers Windows

**Inconvénients:**
- 💰 Plus cher
- 🔑 Token USB physique obligatoire (sécurité renforcée)
- ⏱️ Validation plus longue (3-7 jours)

**Recommandé pour:** Distribution publique, professionnels

---

## 🛒 Étape 1: Acheter un Certificat

### Fournisseurs Recommandés

| Fournisseur | Standard | EV | Lien |
|-------------|----------|----|----|
| **Sectigo** | $200/an | $400/an | https://sectigo.com/ssl-certificates-tls/code-signing |
| **DigiCert** | $300/an | $500/an | https://www.digicert.com/signing/code-signing-certificates |
| **GlobalSign** | $250/an | $400/an | https://www.globalsign.com/en/code-signing-certificate |
| **SSL.com** | $200/an | $400/an | https://www.ssl.com/certificates/code-signing/ |

**Choisir selon votre situation:**
- **Particulier:** Sectigo ou SSL.com (acceptent les particuliers)
- **Entreprise:** DigiCert ou GlobalSign (plus réputés)
- **Budget limité:** Certificat Standard
- **Distribution publique:** Certificat EV

---

### Documents Requis

**Pour un particulier:**
- ✅ Pièce d'identité (passeport ou carte d'identité)
- ✅ Justificatif de domicile
- ✅ Numéro de téléphone (appel de validation)

**Pour une entreprise:**
- ✅ SIRET/Kbis (France) ou équivalent
- ✅ Documents d'incorporation
- ✅ Pièce d'identité du représentant légal
- ✅ Coordonnées vérifiables (téléphone, adresse)

---

### Processus d'Achat (Exemple Sectigo)

1. **Allez sur** https://sectigo.com/ssl-certificates-tls/code-signing
2. **Choisissez:**
   - Code Signing Certificate (Standard)
   - EV Code Signing Certificate (EV)
3. **Sélectionnez** la durée: 1, 2 ou 3 ans
4. **Panier** → Checkout
5. **Remplissez** le formulaire de validation:
   - Informations personnelles/entreprise
   - Coordonnées
   - Type d'organisation
6. **Soumettez** les documents demandés
7. **Attendez** la validation (1-7 jours)
8. **Recevez** le certificat:
   - Standard: Email avec fichier `.pfx`
   - EV: Token USB par courrier

---

## 🔧 Étape 2: Préparer le Certificat

### Certificat Standard (.pfx)

Vous recevez un email avec:
- Fichier `certificate.pfx` (ou `.p12`)
- Mot de passe du certificat

**Placement:**
```
Agent-S/
  desktop-app/
    certificates/
      flemme-codesign.pfx  ← Placez ici
      .gitignore           ← IMPORTANT!
```

**Créer .gitignore:**
```bash
cd desktop-app/certificates
echo "*.pfx" > .gitignore
echo "*.p12" >> .gitignore
```

⚠️ **JAMAIS** commit le certificat dans Git!

---

### Certificat EV (Token USB)

Le certificat est sur un **token USB physique** (YubiKey, etc.).

**Installation:**
1. Branchez le token USB
2. Installez les drivers fournis
3. Configurez le PIN du token
4. Le certificat est accessible via Windows Certificate Store

---

## 🔑 Étape 3: Configurer la Signature

### Méthode 1: Variables d'Environnement (Recommandé)

Créez un fichier `.env.signing` dans `desktop-app/`:

```env
# Certificat Standard (.pfx)
CSC_LINK=C:\Users\tom\Agent-S\desktop-app\certificates\flemme-codesign.pfx
CSC_KEY_PASSWORD=votre_mot_de_passe_certificat

# Ou pour certificat EV (Windows Certificate Store)
# CSC_NAME="Votre Nom ou Entreprise"
```

**⚠️ Sécurité:**
```bash
# Ajoutez à .gitignore
echo ".env.signing" >> .gitignore
```

---

### Méthode 2: Configuration electron-builder.yml

Éditez `desktop-app/electron-builder.yml`:

```yaml
appId: com.flemme.app
productName: Flemme

# ... (autres configs)

win:
  target:
    - target: nsis
      arch:
        - x64
  icon: assets/icon.ico

  # Signature avec fichier .pfx
  certificateFile: certificates/flemme-codesign.pfx
  certificatePassword: ${env.CSC_KEY_PASSWORD}  # Depuis variable d'environnement

  # Ou signature depuis Windows Certificate Store (certificat EV)
  # certificateSubjectName: "Votre Nom ou Entreprise"

  # Configuration de signature
  signDlls: true
  signAndEditExecutable: true
  signingHashAlgorithms:
    - sha256
  rfc3161TimeStampServer: http://timestamp.sectigo.com

  # Alternative timestamp servers:
  # - http://timestamp.digicert.com
  # - http://timestamp.globalsign.com
  # - http://timestamp.comodoca.com

nsis:
  oneClick: false
  allowToChangeInstallationDirectory: true
  createDesktopShortcut: true
  createStartMenuShortcut: true
  shortcutName: Flemme
```

---

### Méthode 3: Script PowerShell

Créez `desktop-app/sign-and-build.ps1`:

```powershell
# Configuration
$env:CSC_LINK = "C:\Users\tom\Agent-S\desktop-app\certificates\flemme-codesign.pfx"
$env:CSC_KEY_PASSWORD = Read-Host -AsSecureString "Mot de passe du certificat"

# Conversion SecureString en texte
$BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($env:CSC_KEY_PASSWORD)
$env:CSC_KEY_PASSWORD = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)

# Build avec signature
npm run build:win -- --config electron-builder.yml

Write-Host "✅ Build signé créé dans dist/"
```

**Utilisation:**
```powershell
cd desktop-app
.\sign-and-build.ps1
# Entrez le mot de passe du certificat quand demandé
```

---

## 🏗️ Étape 4: Builder avec Signature

### Option A: Variables d'Environnement

**PowerShell:**
```powershell
cd desktop-app

# Charger les variables
Get-Content .env.signing | ForEach-Object {
    if ($_ -match '^([^=]+)=(.*)$') {
        [Environment]::SetEnvironmentVariable($matches[1], $matches[2], "Process")
    }
}

# Build
npm run build:win -- --config electron-builder.yml
```

**Bash (Git Bash):**
```bash
cd desktop-app

# Charger les variables
export $(cat .env.signing | xargs)

# Build
npm run build:win -- --config electron-builder.yml
```

---

### Option B: Inline

**PowerShell:**
```powershell
cd desktop-app

$env:CSC_LINK = "C:\chemin\vers\flemme-codesign.pfx"
$env:CSC_KEY_PASSWORD = "votre_mot_de_passe"

npm run build:win -- --config electron-builder.yml
```

---

### Option C: Certificat depuis Windows Store (EV)

**PowerShell:**
```powershell
cd desktop-app

$env:CSC_NAME = "Votre Nom ou Entreprise"

npm run build:win -- --config electron-builder.yml
```

---

## ✅ Étape 5: Vérifier la Signature

### Méthode 1: Propriétés du Fichier

1. Clic droit sur `Flemme Setup 1.0.0.exe`
2. **Propriétés**
3. Onglet **Signatures numériques**
4. Vérifiez:
   - ✅ Nom de l'éditeur
   - ✅ Timestamp présent
   - ✅ Statut: "Cette signature numérique est correcte"

![Signatures numériques](https://i.imgur.com/example.png)

---

### Méthode 2: PowerShell

```powershell
Get-AuthenticodeSignature "dist\Flemme Setup 1.0.0.exe" | Format-List
```

**Résultat attendu:**
```
SignerCertificate : [Subject]
                      CN=Votre Nom ou Entreprise
                    [Issuer]
                      CN=Sectigo Public Code Signing CA
Status            : Valid
StatusMessage     : Signature verified.
TimeStamperCertificate : [Subject]
                         CN=Sectigo Time Stamping Signer
```

---

### Méthode 3: signtool.exe

```powershell
# Installer Windows SDK si besoin
# https://developer.microsoft.com/en-us/windows/downloads/windows-sdk/

& "C:\Program Files (x86)\Windows Kits\10\bin\10.0.22621.0\x64\signtool.exe" verify /pa /v "dist\Flemme Setup 1.0.0.exe"
```

**Résultat attendu:**
```
Verifying: dist\Flemme Setup 1.0.0.exe

Signature Index: 0 (Primary Signature)
Hash of file (sha256): ABC123...
Signing Certificate Chain:
    Issued to: Sectigo Public Code Signing CA
    Issued by: AAA Certificate Services
    Expires:   ...
    SHA1 hash: ...

    Issued to: Votre Nom ou Entreprise
    Issued by: Sectigo Public Code Signing CA
    Expires:   ...
    SHA1 hash: ...

The signature is timestamped: Thu Dec 5 10:30:00 2024
Timestamp Verified by:
    Issued to: Sectigo Time Stamping Signer
    ...

Successfully verified: dist\Flemme Setup 1.0.0.exe
```

---

## 🧪 Étape 6: Tester sur Machine Propre

**⚠️ Important:** Testez sur une machine qui n'a JAMAIS exécuté l'app non signée.

### Test Standard

1. **Machine virtuelle** ou PC propre (Windows 10/11)
2. **Téléchargez** `Flemme Setup 1.0.0.exe` depuis Internet (pas de copie locale)
3. **Double-cliquez** sur l'installateur
4. **Vérifiez:**
   - ✅ Pas d'avertissement SmartScreen
   - ✅ "Éditeur vérifié: Votre Nom" dans l'UAC
   - ✅ Installation normale

---

### Test SmartScreen

**Certificat Standard:**
- ⚠️ Peut afficher "Application non couramment téléchargée"
- ✅ Moins inquiétant qu' "Éditeur inconnu"
- ⏱️ Disparaît après ~1000 installations

**Certificat EV:**
- ✅ Aucun avertissement dès le début
- ✅ Réputation immédiate

---

## 📊 Comparaison: Avec vs Sans Signature

| Aspect | Sans Signature | Certificat Standard | Certificat EV |
|--------|---------------|---------------------|---------------|
| **Avertissement SmartScreen** | ❌ Sévère ("Éditeur inconnu") | ⚠️ Modéré (premiers mois) | ✅ Aucun |
| **Nom éditeur visible** | ❌ Non | ✅ Oui | ✅ Oui |
| **UAC prompt** | ❌ "Éditeur inconnu" | ✅ "Éditeur vérifié" | ✅ "Éditeur vérifié" |
| **Confiance utilisateur** | 😰 20% | 😐 70% | 😊 95% |
| **Téléchargements bloqués** | ⚠️ Fréquent | 🟡 Rare | ✅ Jamais |
| **Coût** | Gratuit | ~$200/an | ~$400/an |
| **Délai validation** | - | 1-3 jours | 3-7 jours |

---

## 💡 Conseils et Astuces

### Construire la Réputation (Certificat Standard)

**SmartScreen nécessite:**
- 📈 Plusieurs milliers de téléchargements
- ✅ Peu de rapports de malware
- ⏱️ ~3-6 mois minimum

**Accélérer le processus:**
1. **Distribuez largement** sur des sites légitimes
2. **GitHub Releases** (plus de confiance)
3. **Signez toutes les versions** (même bêta)
4. **Évitez** les comportements suspects dans l'app
5. **Support réactif** pour rassurer les utilisateurs

---

### Renouvellement du Certificat

**⚠️ Important:** Les certificats expirent après 1-3 ans.

**Avant expiration:**
1. **Achetez** un nouveau certificat (même fournisseur recommandé)
2. **Mettez à jour** la configuration
3. **Resignez** les nouvelles versions
4. **Conservez** l'ancien certificat pour les archives

**Note:** La réputation SmartScreen est liée au certificat. Un nouveau certificat = réputation à reconstruire (sauf EV).

---

### Signer les Mises à Jour

**Si vous utilisez electron-updater:**

Toutes les mises à jour automatiques **doivent être signées** avec le même certificat.

Configuration:
```yaml
# electron-builder.yml
publish:
  provider: github
  owner: votre-username
  repo: flemme

win:
  # Même config de signature
  certificateFile: certificates/flemme-codesign.pfx
  certificatePassword: ${env.CSC_KEY_PASSWORD}
```

---

### Certificat Compromis?

**Si votre certificat .pfx fuite:**

1. **Révoquez immédiatement** auprès du fournisseur
2. **Achetez** un nouveau certificat
3. **Resignez** toutes les versions distribuées
4. **Avertissez** vos utilisateurs

**Prévention:**
- ✅ Ne commitez JAMAIS le .pfx dans Git
- ✅ Stockez dans un emplacement sécurisé
- ✅ Chiffrez le fichier (BitLocker, VeraCrypt)
- ✅ Utilisez un mot de passe fort
- ✅ Limitez l'accès (permissions fichier)

---

## 🚨 Problèmes Courants

### "Failed to sign, certificate not found"

**Causes:**
- Chemin `CSC_LINK` incorrect
- Certificat pas installé dans Windows Store (EV)

**Solutions:**
```powershell
# Vérifier le chemin
Test-Path "C:\chemin\vers\certificat.pfx"  # Doit retourner True

# Lister les certificats installés (EV)
Get-ChildItem -Path Cert:\CurrentUser\My
```

---

### "The specified timestamp server either could not be reached"

**Cause:** Serveur de timestamp injoignable

**Solution:** Changez le serveur dans `electron-builder.yml`:
```yaml
win:
  rfc3161TimeStampServer: http://timestamp.digicert.com
  # Alternatives:
  # http://timestamp.sectigo.com
  # http://timestamp.globalsign.com
  # http://timestamp.comodoca.com
```

---

### "Invalid password for certificate"

**Solution:**
```powershell
# Vérifier le mot de passe
$password = Read-Host -AsSecureString "Mot de passe"
$cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2
$cert.Import("chemin\vers\cert.pfx", $password, "Exportable")
$cert  # Doit afficher les infos du certificat
```

---

### Avertissement SmartScreen Persiste (Certificat Standard)

**Normal!** Réputation à construire.

**Solutions:**
1. **Patience:** 3-6 mois avec distribution active
2. **Certificat EV:** Réputation immédiate
3. **Documentation:** Expliquez aux utilisateurs que c'est normal
4. **Support:** Aidez les utilisateurs effrayés

---

## 📚 Ressources Supplémentaires

**electron-builder Code Signing:**
https://www.electron.build/code-signing

**Microsoft SmartScreen:**
https://docs.microsoft.com/en-us/windows/security/threat-protection/windows-defender-smartscreen

**Sectigo Code Signing Guide:**
https://sectigo.com/knowledge-base/detail/Code-Signing-Certificate-Installation/kA01N000000zFKp

**Windows signtool.exe:**
https://docs.microsoft.com/en-us/windows/win32/seccrypto/signtool

---

## ✅ Checklist de Signature

Avant de distribuer:

- [ ] Certificat acheté et validé
- [ ] Certificat installé (.pfx ou token USB)
- [ ] Configuration electron-builder.yml mise à jour
- [ ] Variables d'environnement configurées
- [ ] .gitignore inclut le certificat
- [ ] Build signé créé
- [ ] Signature vérifiée (Propriétés → Signatures numériques)
- [ ] Timestamp présent et valide
- [ ] Testé sur machine propre
- [ ] Aucun avertissement SmartScreen (EV) ou avertissement modéré (Standard)
- [ ] Documentation utilisateur mise à jour

---

## 💰 Budget et ROI

### Coûts

**Certificat Standard:**
- $200/an × 3 ans = **$600**

**Certificat EV:**
- $400/an × 3 ans = **$1,200**

**Alternative gratuite:**
- $0 mais ~50% des utilisateurs abandonnent l'installation

---

### Retour sur Investissement

**Avec signature:**
- ✅ Taux d'installation: ~90%
- ✅ Confiance utilisateur: Élevée
- ✅ Support réduit (moins de questions)
- ✅ Image professionnelle

**Sans signature:**
- ❌ Taux d'installation: ~40%
- ❌ Confiance utilisateur: Faible
- ❌ Support élevé (beaucoup de questions)
- ❌ Image amateur

**Conclusion:** La signature est **essentielle** pour distribution publique.

---

## 🎯 Recommandation Finale

### Pour Flemme:

**Si distribution publique (recommandé):**
- ✅ **Certificat EV** ($400/an)
- ✅ Réputation immédiate
- ✅ Aucun avertissement
- ✅ Image professionnelle

**Si distribution limitée (amis/entreprise):**
- 🟡 **Certificat Standard** ($200/an)
- 🟡 Avertissements au début
- 🟡 Documentation nécessaire
- 🟡 Acceptable pour petit volume

**Si prototype/test:**
- ⚠️ **Pas de signature** (gratuit)
- ⚠️ Seulement pour développement
- ⚠️ Pas pour distribution publique

---

**Bonne signature! 🔐✨**
