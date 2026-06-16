# n8n Credentials Setup Guide

## 1. Meta Graph API (required for all 3 workflows)

1. Go to **Settings → Credentials → Add Credential**
2. Choose **Query Auth** (type: `Generic Credential Type`)
3. Name: `Meta Graph API`
4. Set **Node Credentials Type** to `Generic Credential Type`
5. Configure:
   - **Auth Type**: `Query Auth`
   - **Name**: `access_token`
   - **Value**: `<your Instagram Page Access Token>`

### Getting your Page Access Token
1. Go to [Facebook Developers](https://developers.facebook.com/apps/)
2. Open your app → **Tools** → **Graph API Explorer**
3. Select your app + **Page** token
4. Permissions needed: `instagram_basic`, `instagram_manage_messages`, `instagram_content_publish`, `pages_messaging`, `pages_read_engagement`
5. Copy the long-lived token (60 days)

### Getting your Instagram Business Account ID
1. Call: `GET /v21.0/me/accounts?fields=instagram_business_account`
2. Or search for it in Graph API Explorer
3. Set it in each workflow's **static data** (see below)

## 2. Google Sheets (Workflow 2)

1. **Settings → Credentials → Add Credential**
2. Choose **Google Sheets OAuth2 API**
3. Name: `Google Sheets OAuth2`
4. Follow Google's OAuth consent screen setup:
   - Create credentials in [Google Cloud Console](https://console.cloud.google.com/)
   - Add `https://www.googleapis.com/auth/spreadsheets` scope
   - Add `https://www.googleapis.com/auth/drive.file` scope
   - Set redirect URI to `https://<your-n8n-url>/rest/oauth2-credential/callback`
5. Paste **Client ID** and **Client Secret** into n8n

## 3. SMTP / Email (Workflow 3)

**Option A: Gmail (free)**
1. Enable 2FA on your Google account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. In n8n: **Settings → Credentials → Add Credential → SMTP**
4. Set:
   - Host: `smtp.gmail.com`
   - Port: `465`
   - SSL: `true`
   - User: your email
   - Password: the app password

**Option B: Any free SMTP** (SendGrid, Mailgun free tiers, etc.)

---

## Setting Workflow Static Data (per workflow)

After import, you need to set these variables in each workflow:

### Workflow 1 — Comment-to-DM
1. Open workflow → **Workflow Settings** tab
2. In the Code node `Extract & Filter Comments`, add:
   ```
   $getWorkflowStaticData('global').igBusinessId = 'YOUR_IG_BUSINESS_ID';
   ```
3. Execute manually once to persist, then remove the line

### Workflow 2 — Content Pipeline
The Code node `Filter Unpublished` reads:
- `$getWorkflowStaticData('global').googleSheetId` — your Google Sheet ID (long string from URL)
- `$getWorkflowStaticData('global').sheetName` — default `Sheet1`

### Workflow 3 — Daily Analytics
The Code node `Detect Spikes` reads:
- `$getWorkflowStaticData('global').thresholds` — spike alert thresholds
- Configure email addresses in the `Send Email Alert` node

---

## Google Sheet Structure (Workflow 2)

Create a sheet with these column headers (row 1):

| hardware_spec | network_concept | post_type | image_url | id |
|---|---|---|---|---|
| 4K CCTV camera | PoE switch installation | image | https://... | 1 |
| Smart door lock | WiFi vs Z-Wave comparison | carousel | https://... | 2 |

---

## Importing Workflows

1. n8n UI → **Workflows** → **Add Workflow** → **Import from File**
2. Select the JSON file
3. Create all credentials first, then update the credential references if needed
