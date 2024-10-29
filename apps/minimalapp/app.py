"""
validate_email, EmailNotValidError: 이메일 주소 형식 체크용
Flask: flask 클래스를 import 
render_template: 기본 템플릿 엔진: Jinja2를 사용하여 HTML을 렌더링
url_for: endpoint의 url 이용
current_app: 애플리케이션 컨텍스트 - 액티브 앱의 인스턴스 
g: 애플리케이션 컨텍스트 - 요청을 통해 이용 가능한 전역 임시 영역. 요청마다 리셋
request: 요청 컨텍스트 - 요청이 있는 동안 요청 레벨의 데이터 이용 가능 = 요청 정보 취득
redirect: 다른 엔드포인트로 리다이렉트하려면 redirect 함수를 사용합니다.
	import 문이 길어지기 때문에 줄바꿈
flash: 동작 실행 후 간단한 메시지를 표시하는 기능.
	1. flash 함수 설정
	2. 템플릿에서 get_flashed_messages 함수 사용해 취득하여 표시
	3. Flash 메시지를 이용하려면 세션(정보를 서버에 유지 + 일련의 처리를 계속 실시)이 필요하므로 config의 SECRET_KEY 설정 필요
"""
from email_validator import validate_email, EmailNotValidError
from flask import (
	Flask, 
	render_template, 
	url_for, 
	current_app, 
	g, 
	request, 
	redirect, 
	flash,
) 


# flask 클래스를 인스턴스화한다.
app = Flask(__name__)


# URL과 실행할 함수를 매핑한다.
@app.route("/")
def index():
	return "Hello, Flaskbook!"


@app.route(	"/hello/<name>",
	# methods에 HTTP 메서드를 기술함으로써 이 함수는 두개의 메서드의 요청을 받을 수 있다.
	methods=["GET", "POST"],
	endpoint="hello-endpoint")
def hello(name):
	return f"Hello, {name}!"


# show_name 엔드포인트를 작성한다.
@app.route("/name/<name>")
def show_name(name):
	# 변수를 템플릿 엔진에게 건넨다.
	return render_template("index.html", name=name)


with app.test_request_context():
	# /
	print(url_for("index"))
	# /hello/world
	print(url_for("hello-endpoint", name="world"))
	# /name/AK?page=1
	print(url_for("show_name", name="AK", page="1"))


# 여기에서 호출하면 오류가 된다.
# print(current_app)

# 애플리케이션 컨텍스트를 취득하여 스택에 push한다.
ctx = app.app_context()
ctx.push()

# current_app에 접근할 수 있게 된다.
print(current_app.name)
# >> apps.minimalapp.app

# 전역 임시 영역에 값을 설정한다.
g.connection = "connection"
print(g.connection)
# >> connection


# 요청 컨텍스트 수동 취득하여 푸시
with app.test_request_context("/users?updated=true"):
	# true가 출력된다.
	print(request.args.get("updated"))


# 문의 폼 화면 반환
@app.route("/contact")
def contact():
	return render_template("contact.html")


# 문의 폼 처리 & 문의 완료 화면 반환하는 엔드포인트 만듦. 2번째 인수에 GET, POST 허가 
@app.route("/contact/complete", methods=["GET", "POST"])
def contact_complete():
	# request.method 속성을 이용하여 요청된 메서드 확인
	if request.method == "POST":
		# form 속성을 사용해서 POST된 폼의 값을 취득한다.
		username = request.form["username"]
		email = request.form["email"]
		description = request.form["description"]


		# 입력 체크
		is_valid = True


		if not username:
			flash("사용자명은 필수입니다.")
			is_valid = False


		if not email:
			flash("메일 주소는 필수입니다.")
			is_valid = False

		
		try:
			validate_email(email)
		except EmailNotValidError:
			flash("메일 주소의 형식으로 입력해 주세요")
			is_valid = False


		if not description:
			flash("문의 내용은 필수입니다.")
			is_valid = False


		if not is_valid:
			return redirect(url_for("contact"))
		# 이메일을 보낸다(나중에 구현할 부분)


		# 문의 완료 엔드포인트로 리다이렉트 한다.
		flash("문의해 주셔서 감사합니다.")


		# POST의 경우, 문의 완료 엔드포인트를 contact 엔드포인트로 리다이렉트 한다.
		return redirect(url_for("contact_complete"))
	
	# GET의 경우, 문의 완료 화면을 contact 엔드포인트로 리다이렉트 한다.
	return render_template("contact_complete.html")



app = Flask(__name__)
# SECRET_KEY를 추가한다.
app.config["SECRET_KEY"] = "2AZSMss3p5QPbcY2hBsJ"