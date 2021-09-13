var image = document.getElementById("image");
var title = document.getElementById("title");
var imageFile = document.getElementById("file");
var content = document.getElementById("content");
var category = document.getElementById("category");
var alertBox = document.getElementById("alert-box");
var form = document.getElementById("update-blog-form");
var csrf = document.getElementsByName("csrfmiddlewaretoken");
var blogId = window.location.href.split("/")[4];

fetch(`http://127.0.0.1:8000/get-blog/${blogId}`, {
  method: "GET",
})
  .then((res) => res.json())
  .then((res) => {
    const blog = res.find((item) => {
      return item.pk == blogId;
    });
    title.value = blog.fields.title;
    content.value = blog.fields.content;
    category.value = blog.fields.category;
    image.src = "/media/" + blog.fields.image;
  })
  .catch((err) => {
    console.log(err);
  });

const showAlert = (type, message) => {
  alertBox.innerHTML = `<div class="alert alert-${type} alert-dismissible fade show" role="alert">
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
      </div>`;
};

imageFile.addEventListener("change", () => {
  const url = URL.createObjectURL(imageFile.files[0]);
  image.src = url;
});

form.addEventListener("submit", (e) => {
  e.preventDefault();
  const fd = new FormData();
  fd.append("title", title.value);
  fd.append("content", content.value);
  fd.append("category", category.value);
  console.log(imageFile.files[0]);
  if (imageFile.files[0]) {
    fd.append("image", imageFile.files[0]);
  }
  fd.append("csrfmiddlewaretoken", csrf[0].value);
  fetch(`http://127.0.0.1:8000/update-blog/${blogId}`, {
    method: "POST",
    body: fd,
  })
    .then((res) => res.json())
    .then((res) => {
      showAlert("success", res.message);
      setTimeout(() => {
        window.location.href = "http://127.0.0.1:8000/user-blog";
      }, 3000);
    })
    .catch((err) => {
      console.log(err);
      showAlert("danger", "Blog created failed");
    });
});
