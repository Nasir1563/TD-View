from supabase import create_client, Client

SUPABASE_URL = 'https://bpmwaznhgealzdigaokn.supabase.co'
SUPABASE_KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImJwbXdhem5oZ2VhbHpkaWdhb2tuIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTgxMzM3MzgsImV4cCI6MjAzMzcwOTczOH0.ISUBgMoBUFPBJd73PlhqwyCBTYW5fFwM9GoIbeRPdlg'

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)