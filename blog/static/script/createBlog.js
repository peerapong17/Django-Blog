var image = document.getElementById("image");
var title = document.getElementById("title");
var imageFile = document.getElementById("file");
var content = document.getElementById("content");
var category = document.getElementById("category");
var alertBox = document.getElementById("alert-box");
var form = document.getElementById("create-blog-form");
var csrf = document.getElementsByName("csrfmiddlewaretoken");

const showAlert = (type, message) => {
  alertBox.innerHTML = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>`;
};

imageFile.addEventListener("change", () => {
  const url = URL.createObjectURL(imageFile.files[0]);
  console.log(imageFile.files[0]);
  image.removeAttribute("image");
  image.id = "show-image";
  image.src = url;
});

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const fd = new FormData();
  fd.append("title", title.value);
  fd.append("content", content.value);
  fd.append("category", category.value);
  fd.append("image", imageFile.files[0]);
  fd.append("csrfmiddlewaretoken", csrf[0].value);
  fetch("http://127.0.0.1:8000/create-blog", {
    method: "POST",
    body: fd,
  })
    .then((res) => res.json())
    .then((res) => {
      showAlert("success", res.message);
      setTimeout(() => {
        window.location.href = "http://127.0.0.1:8000/";
      }, 3000);
    })
    .catch((err) => {
      console.log(err);
      showAlert("danger", "Blog created failed");
    });
});
