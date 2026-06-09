
## Setup flow

1. **Fork the GitHub repo** so you have your own copy to edit and deploy.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
2. **Open the project in an IDE** like VS Code or Cursor.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
3. **Clone the repo** into your local folder with Git.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
4. Run **npm install** to install dependencies.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
5. Copy **`.env.local.example`** to **`.env.local`**.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
6. Add these Supabase values into `.env.local`:
    
    - `SUPABASE_URL`
        
    - `SUPABASE_ANON_KEY`
        
    - `SUPABASE_SERVICE_ROLE_KEY`
        
    - encryption key from the provided code snippet.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
        
7. Run the app locally with **npm run dev**.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
8. Open the local app in the browser and create your account; it will work only after Supabase is configured.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
9. In **Supabase**, create a new project.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
10. Copy the **project URL** and paste it into the app’s Supabase config.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
11. Go to **Project Settings → API** and copy the **anon key** and **service role key** into `.env.local`.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
12. Generate the **encryption key** from the code shown in the video and paste it into `.env.local`.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
13. Restart the server and confirm the dashboard loads.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
14. In the app, go to **Settings → WhatsApp Config**.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
15. In Meta Developer App, open **App Settings → Basic** and copy the **App Secret** into WACRM.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
16. In Meta App, open **API Setup** and copy the **Phone Number ID** and **Business Account ID** into WACRM.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
17. Paste your **permanent access token** into WACRM.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
18. Set any text as the **verify token**, then click **Save Configuration**.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
19. Open **Supabase Table Editor** and confirm the WhatsApp config record exists; if needed, create tables by running the SQL migrations one by one or via `supabase db push`.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
20. Click **Test API Connection** to confirm the Meta connection is working.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
21. Start **ngrok** with your local port, such as `ngrok http 3000`, to get an HTTPS URL.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
22. In Meta webhook settings, set the callback URL to:  
    `your-ngrok-url/api/whatsapp/webhook`.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
23. Enter the same **verify token** and click **Verify and Save**.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
24. Send a test WhatsApp message and check that it appears in the WACRM inbox.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
25. For 24/7 use, deploy the app to a VPS/hosting provider as a **Node.js web app**.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
26. Add all `.env.local` values as hosting environment variables.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    
27. Deploy the app and then sign in on the live domain.[](https://github.com/ObinnaIheanachor/Whatsapp-Chat-project/blob/master/README.md)
    

## What the video says it supports

The video says the app includes dashboard, inbox, contacts, pipeline, broadcast, automations, settings, templates, tags, and WhatsApp config. It also says the automations include welcome message, out-of-office, lead qualifier, and follow-up reminder workflows