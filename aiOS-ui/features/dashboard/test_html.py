from main import DASHBOARD_HTML
print("HTML length:", len(DASHBOARD_HTML))
with open("dump.html", "w") as f:
    f.write(DASHBOARD_HTML)
