import tkinter as tk
import subprocess

class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Web Scraper App")

        self.run_button = tk.Button(root, text="Lấy Dữ Liệu", command=self.run_scraper)
        self.run_button.pack()

    def run_scraper(self):
        try:
            subprocess.run(["scrapy", "crawl", "chocolatespider"])
            print("Thu thập dữ liệu hoàn thành.")
        except Exception as e:
            print("Lỗi khi chạy scraper:", e)

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()
