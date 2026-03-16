// Populate the sidebar
//
// This is a script, and not included directly in the page, to control the total size of the book.
// The TOC contains an entry for each page, so if each page includes a copy of the TOC,
// the total size of the page becomes O(n**2).
class MDBookSidebarScrollbox extends HTMLElement {
    constructor() {
        super();
    }
    connectedCallback() {
        this.innerHTML = '<ol class="chapter"><li class="chapter-item expanded "><a href="intro/intro.html"><strong aria-hidden="true">1.</strong> Introduction</a></li><li><ol class="section"><li class="chapter-item expanded "><a href="intro/whois.html"><strong aria-hidden="true">1.1.</strong> Who is Herbert</a></li><li class="chapter-item expanded "><a href="intro/slides.html"><strong aria-hidden="true">1.2.</strong> Slides and Code Repo</a></li><li class="chapter-item expanded "><a href="intro/python_awesome.html"><strong aria-hidden="true">1.3.</strong> Python is Awesome</a></li><li class="chapter-item expanded "><a href="intro/python_slow.html"><strong aria-hidden="true">1.4.</strong> Python can be Slow</a></li><li class="chapter-item expanded "><a href="intro/outro.html"><strong aria-hidden="true">1.5.</strong> Outro</a></li></ol></li><li class="chapter-item expanded "><a href="pyo3/intro.html"><strong aria-hidden="true">2.</strong> Introducing PyO3</a></li><li><ol class="section"><li class="chapter-item expanded "><a href="pyo3/how_python_libs_work.html"><strong aria-hidden="true">2.1.</strong> How Python Libraries Work</a></li><li class="chapter-item expanded "><a href="pyo3/setup/intro.html"><strong aria-hidden="true">2.2.</strong> PyO3 Setup - Maturin</a></li><li><ol class="section"><li class="chapter-item expanded "><a href="pyo3/setup/venv.html"><strong aria-hidden="true">2.2.1.</strong> Let&#39;s Make a Virtual Environment (venv)</a></li><li class="chapter-item expanded "><a href="pyo3/setup/install_maturin.html"><strong aria-hidden="true">2.2.2.</strong> Install Maturin</a></li><li class="chapter-item expanded "><a href="pyo3/setup/what_does_it_do.html"><strong aria-hidden="true">2.2.3.</strong> What does it do?</a></li><li class="chapter-item expanded "><a href="pyo3/setup/hello_world.html"><strong aria-hidden="true">2.2.4.</strong> Add Hello World</a></li><li class="chapter-item expanded "><a href="pyo3/setup/pyresult.html"><strong aria-hidden="true">2.2.5.</strong> All About PyResult</a></li><li class="chapter-item expanded "><a href="pyo3/setup/params.html"><strong aria-hidden="true">2.2.6.</strong> Passing Rust Types as Parameters</a></li></ol></li><li class="chapter-item expanded "><a href="pyo3/fib/intro.html"><strong aria-hidden="true">2.3.</strong> Fibonacci Numbers - Slow!</a></li><li><ol class="section"><li class="chapter-item expanded "><a href="pyo3/fib/slow_fib.html"><strong aria-hidden="true">2.3.1.</strong> Really Slow Python Fibonacci</a></li><li class="chapter-item expanded "><a href="pyo3/fib/rust1.html"><strong aria-hidden="true">2.3.2.</strong> Let&#39;s Port that to Rust</a></li><li class="chapter-item expanded "><a href="pyo3/fib/rust2.html"><strong aria-hidden="true">2.3.3.</strong> We can do better - Rayon!</a></li></ol></li><li class="chapter-item expanded "><a href="pyo3/classes.html"><strong aria-hidden="true">2.4.</strong> Python Classes</a></li><li class="chapter-item expanded "><div><strong aria-hidden="true">2.5.</strong> Fun Mandelbrot Finale</div></li><li><ol class="section"><li class="chapter-item expanded "><div><strong aria-hidden="true">2.5.1.</strong> Python Mandelbrot</div></li><li class="chapter-item expanded "><div><strong aria-hidden="true">2.5.2.</strong> Rust-Python Mandelbrot</div></li></ol></li></ol></li><li class="chapter-item expanded "><div><strong aria-hidden="true">3.</strong> Wrap Up</div></li></ol>';
        // Set the current, active page, and reveal it if it's hidden
        let current_page = document.location.href.toString().split("#")[0].split("?")[0];
        if (current_page.endsWith("/")) {
            current_page += "index.html";
        }
        var links = Array.prototype.slice.call(this.querySelectorAll("a"));
        var l = links.length;
        for (var i = 0; i < l; ++i) {
            var link = links[i];
            var href = link.getAttribute("href");
            if (href && !href.startsWith("#") && !/^(?:[a-z+]+:)?\/\//.test(href)) {
                link.href = path_to_root + href;
            }
            // The "index" page is supposed to alias the first chapter in the book.
            if (link.href === current_page || (i === 0 && path_to_root === "" && current_page.endsWith("/index.html"))) {
                link.classList.add("active");
                var parent = link.parentElement;
                if (parent && parent.classList.contains("chapter-item")) {
                    parent.classList.add("expanded");
                }
                while (parent) {
                    if (parent.tagName === "LI" && parent.previousElementSibling) {
                        if (parent.previousElementSibling.classList.contains("chapter-item")) {
                            parent.previousElementSibling.classList.add("expanded");
                        }
                    }
                    parent = parent.parentElement;
                }
            }
        }
        // Track and set sidebar scroll position
        this.addEventListener('click', function(e) {
            if (e.target.tagName === 'A') {
                sessionStorage.setItem('sidebar-scroll', this.scrollTop);
            }
        }, { passive: true });
        var sidebarScrollTop = sessionStorage.getItem('sidebar-scroll');
        sessionStorage.removeItem('sidebar-scroll');
        if (sidebarScrollTop) {
            // preserve sidebar scroll position when navigating via links within sidebar
            this.scrollTop = sidebarScrollTop;
        } else {
            // scroll sidebar to current active section when navigating via "next/previous chapter" buttons
            var activeSection = document.querySelector('#sidebar .active');
            if (activeSection) {
                activeSection.scrollIntoView({ block: 'center' });
            }
        }
        // Toggle buttons
        var sidebarAnchorToggles = document.querySelectorAll('#sidebar a.toggle');
        function toggleSection(ev) {
            ev.currentTarget.parentElement.classList.toggle('expanded');
        }
        Array.from(sidebarAnchorToggles).forEach(function (el) {
            el.addEventListener('click', toggleSection);
        });
    }
}
window.customElements.define("mdbook-sidebar-scrollbox", MDBookSidebarScrollbox);
