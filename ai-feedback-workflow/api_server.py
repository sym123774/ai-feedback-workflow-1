"""
AI 用户反馈分析 - API 服务器
提供 HTTP API 接口
"""

from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from ai_workflow import FeedbackAnalyzer

analyzer = FeedbackAnalyzer()


class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path == "/analyze":
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                feedback_list = data.get("feedback_list", [])
                
                if not feedback_list:
                    self.send_error(400, "feedback_list is required")
                    return
                
                results = analyzer.analyze_batch(feedback_list)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(results, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                self.send_error(500, str(e))
        else:
            self.send_error(404, "Not Found")
    
    def do_GET(self):
        if self.path == "/health":
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            self.wfile.write(b'{"status": "ok"}')
        else:
            self.send_error(404, "Not Found")
    
    def log_message(self, format, *args):
        print(f"[API] {args[0]}")


def run_server(port=8000):
    server = HTTPServer(('localhost', port), RequestHandler)
    print(f"API Server running at http://localhost:{port}")
    print("Endpoints:")
    print("  POST /analyze - 分析用户反馈")
    print("  GET  /health  - 健康检查")
    print("\n示例调用:")
    print('  curl -X POST http://localhost:8000/analyze \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"feedback_list": ["反馈内容"]}\'')
    server.serve_forever()


if __name__ == "__main__":
    run_server()
