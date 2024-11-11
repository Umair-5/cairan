const header = document.querySelector("#header");
let lastScrollY = window.scrollY;

const onScrollDown = () => {
    header.classList.remove("header")
};

const onScrollUp = () => {
    header.classList.add("header")
};

window.addEventListener("scroll", function () {
    const currentScrollY = window.scrollY;
    if (currentScrollY > lastScrollY + 10) {
        onScrollDown();
    }
    else if (currentScrollY < lastScrollY - 15) {
        onScrollUp();
    }
    lastScrollY = currentScrollY;
});

