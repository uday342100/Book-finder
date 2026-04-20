Smart Library Navigator - Vercel Deployment Folder

This folder is prepared for direct Vercel deployment.

Path:
d:\Udayyy\Desktop\Smart-Library-Navigator-Vercel

How to deploy:
1) Open terminal in this folder
2) Run:
   vercel login
   vercel --prod

Notes:
- Vercel will use `api/index.py` as the web entrypoint (configured in `vercel.json`).
- Streamlit source files are also included (`app.py`, `data.py`, etc.) for local/demo use.
- For local Streamlit run:
   pip install -r requirements.txt
   streamlit run app.py
