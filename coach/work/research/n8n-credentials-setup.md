# n8n Credentials Setup Guide

## Important: After importing any workflow JSON

The JSON files have **placeholder credential IDs** (`__CREDENTIAL_META_GRAPH_API__`, etc.).
You must create real credentials in n8n first, then manually link them:

1. **Settings → Credentials** → create each credential below
2. Open the workflow → each node with a red error badge → click the credential field
3. Select the credential you created from the dropdown
4. **Save** the workflow

---

## 1. Meta Graph API (required for ALL workflows)

### Step 1 — Get a Page Access Token

1. Go to [developers.facebook.com/apps](https://developers.facebook.com/apps/)
2. Open your app → **Tools** → **Graph API Explorer**
3. Select your app, set token type to **Page Token**, pick your Facebook Page
4. Click **Add Permission** and add these (use the search bar to find each):
   - `pages_manage_posts`
   - `pages_read_engagement`
   - `pages_messaging`
   - `instagram_basic`
   - `instagram_manage_messages`
   - `instagram_content_publish`
5. Click **Generate Access Token** → copy the token that appears
   - This token expires in ~60 days. Set a calendar reminder to refresh it.

### Step 2 — Create the credential in n8n

1. n8n → **Settings** → **Credentials** → **Add Credential**
2. Search for **Query Auth** (it's under "Generic Credential Type")
3. Name: `Meta Graph API`
4. **Auth Type**: `Query Auth`
5. **Name**: `access_token`
6. **Value**: paste the token from Step 1
7. Click **Save**

### Step 3 — Get your Instagram Business Account ID

1. In Graph API Explorer (same page), change the dropdown to `GET` and run:
   `GET /v21.0/me/accounts?fields=instagram_business_account`
2. Look for `instagram_business_account` → `id` in the response
3. Copy that ID — you'll set it in each workflow's static data

---

## 2. Google Sheets OAuth2 (Workflow 2 — Content Pipeline)

1. n8n → **Settings** → **Credentials** → **Add Credential**
2. Search for **Google Sheets OAuth2 API**
3. Name: `Google Sheets OAuth2`
4. Go to [Google Cloud Console](https://console.cloud.google.com/)
5. Create a project (or select existing) → **APIs & Services** → **Credentials**
6. Click **Create Credentials** → **OAuth Client ID**
7. Application type: **Web application**
8. Add redirect URI: `https://<your-n8n-url>/rest/oauth2-credential/callback`
   - If running locally: `http://localhost:5678/rest/oauth2-credential/callback`
9. Copy **Client ID** and **Client Secret** into n8n
10. Click **Save** → then **Connect Account** and sign in with Google

---

## 3. SMTP / Email (Workflow 3 — Analytics Alerts)

**Option A: Gmail (free)**

1. Enable 2FA on your Google account
2. Generate an [App Password](https://myaccount.google.com/apppasswords)
3. In n8n: **Settings → Credentials → Add Credential → SMTP**
4. Set:
   - **Host**: `smtp.gmail.com`
   - **Port**: `465`
   - **SSL**: `true`
   - **User**: your Gmail address
   - **Password**: the app password (16 characters, no spaces)
5. Click **Save**

**Option B: SendGrid or Mailgun free tier** — same SMTP flow, different host/port.

---

## Setting Workflow Static Data (per workflow)

After importing and linking credentials, set these variables:

### Workflow 1 — Comment-to-DM (Instagram)
1. Open the Code node `Extract & Filter Comments`
2. Add this at the top of the JS code:
   ```javascript
   $getWorkflowStaticData('global').igBusinessId = 'YOUR_IG_BUSINESS_ID';
   ```
3. Execute the workflow manually once to persist the value
4. Remove the line (the value is now saved)

### Facebook Page Comment to DM
1. In the Code node `Extract & Filter Comments`, add:
   ```javascript
   $getWorkflowStaticData('global').facebookPageId = 'YOUR_FB_PAGE_ID';
   ```
2. Same persist step: run once, then remove

### Workflow 2 — Content Pipeline
In the Code node `Filter Unpublished`, set:
- `$getWorkflowStaticData('global').googleSheetId` — the long string from your Sheet URL
- `$getWorkflowStaticData('global').sheetName` — default `Sheet1`

### Workflow 3 — Daily Analytics
In Code node `Detect Spikes`:
- `$getWorkflowStaticData('global').thresholds` — optional, defaults to 10% follower, 50% reach/impression

In email node `Send Email Alert`:
- Set `fromEmail` and `toEmail` in the node parameters (or use static data)

---

## Google Sheet Structure (Workflow 2)

Create a sheet with these column headers in row 1:

| hardware_spec | network_concept | post_type | image_url | id |
|---|---|---|---|---|
| 4K CCTV camera | PoE switch installation | image | https://... | 1 |
| Smart door lock | WiFi vs Z-Wave comparison | carousel | https://... | 2 |

---

## Importing Workflows

1. n8n UI → **Workflows** → **Add Workflow** → **Import from File**
2. Select the JSON file
3. **IMPORTANT**: After import, link each node's credential (they'll show red errors)
4. Set static data values (see above)
5. Test with **Execute Workflow** button before activating the trigger

---

## Troubleshooting

| Error | Likely cause |
|---|---|
| "Invalid credentials" / red badge on node | Credential not linked — open node, select the right credential |
| 401 Unauthorized from Graph API | Token expired or missing permissions — re-generate in Graph API Explorer |
| 403 Forbidden | Token doesn't have the required permission scope |
| Ollama connection refused | n8n running outside Docker? Change URL to `http://localhost:11434/api/generate` |
| "Cannot read properties of undefined" | Static data not set — add `igBusinessId` or `facebookPageId` |

### Token Refresh Reminder
Facebook Page Access Tokens last **60 days**. Set a reminder to refresh it:
1. Go to Graph API Explorer
2. Click **Generate Access Token** again (same permissions)
3. Update the credential value in n8n Settings
