console.log(this.window);

const toggleMobileMenu = () => {
    let menu = document.getElementById("mobilemenu");
    menu.classList = [
        (menu.classList.contains("mobilemenuhidden") ? "mobilemenushown" : "mobilemenuhidden")
    ];
    menu.classList.add("hide-on-large-only");
};