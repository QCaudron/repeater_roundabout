export { Tabs };

class Tabs {
    outer: HTMLUListElement;
    tabs: HTMLLIElement[] = [];
    content: HTMLElement[] = [];
    parent: HTMLElement;
    selection: number | undefined;

    constructor(parent: HTMLElement) {
        this.outer = document.createElement('ul');
        this.outer.className = 'tabs';
        parent.appendChild(this.outer);
        this.parent = parent;
    }

    addTab(name: string, content: HTMLElement) {
        let tab = document.createElement('li');
        tab.innerText = name;
        this.tabs.push(tab);
        this.outer.appendChild(tab);

        content.style.display = 'none';
        this.content.push(content);

        tab.addEventListener('click', () => {
            this.select(this.tabs.indexOf(tab));
        });
    }

    injectContent() {
        for (let c of this.content) {
            this.parent.appendChild(c);
        }
        this.select(0);
    }

    select(index: number) {
        if (this.selection !== undefined) {
            this.tabs[this.selection].classList.remove('selected');
            this.content[this.selection].style.display = 'none';
        }

        this.tabs[index].classList.add('selected');
        this.content[index].style.display = 'block';
        this.selection = index;
    }
}
