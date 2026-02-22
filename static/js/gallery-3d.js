// 3D Scroll Gallery - Based on Codrops "On-Scroll Perspective Grid Animations"
// Uses GSAP + ScrollTrigger

(function() {
    const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (prefersReducedMotion) return;

    const w = window.innerWidth;

    // Three tiers: small mobile, tablet, desktop
    const params = w <= 480 ? {
        zMin: -100, zMax: 50,
        xFromMin: -200, xFromMax: -80,
        xToMin: 80, xToMax: 200,
        yFromMin: 30, yFromMax: 80,
        yToMin: -80, yToMax: -30,
        rotationY: 8,
        scrub: 2.5
    } : w <= 768 ? {
        zMin: -300, zMax: 100,
        xFromMin: -400, xFromMax: -200,
        xToMin: 200, xToMax: 400,
        yFromMin: 50, yFromMax: 120,
        yToMin: -120, yToMax: -50,
        rotationY: 12,
        scrub: 2.5
    } : {
        zMin: -800, zMax: 200,
        xFromMin: -1000, xFromMax: -500,
        xToMin: 500, xToMax: 1000,
        yFromMin: 100, yFromMax: 300,
        yToMin: -300, yToMax: -100,
        rotationY: 25,
        scrub: 2
    };

    const lazyLoadImages = () => {
        const items = document.querySelectorAll('.grid__item-inner[data-bg]');
        if (!items.length) return Promise.resolve();

        return new Promise((resolve) => {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const el = entry.target;
                        el.style.backgroundImage = `url('${el.dataset.bg}')`;
                        el.removeAttribute('data-bg');
                        observer.unobserve(el);
                    }
                });
            }, { rootMargin: '200% 0px' });

            items.forEach(item => observer.observe(item));
            imagesLoaded(document.querySelectorAll('.grid__item-inner'), { background: true }, resolve);
        });
    };

    const applyGalleryAnimation = () => {
        const grid = document.querySelector('.grid--gallery');
        if (!grid) return;

        const gridWrap = grid.querySelector('.grid-wrap');
        const gridItems = grid.querySelectorAll('.grid__item');
        const count = gridItems.length;

        // Pre-compute all random values once so they never change
        const zValues = [];
        const xFrom = [], xTo = [];
        const yFrom = [], yTo = [];
        for (let i = 0; i < count; i++) {
            zValues.push(gsap.utils.random(params.zMin, params.zMax));
            xFrom.push(gsap.utils.random(params.xFromMin, params.xFromMax));
            xTo.push(gsap.utils.random(params.xToMin, params.xToMax));
            yFrom.push(gsap.utils.random(params.yFromMin, params.yFromMax));
            yTo.push(gsap.utils.random(params.yToMin, params.yToMax));
        }

        // Set static properties outside the timeline
        gsap.set(gridWrap, {
            rotationY: params.rotationY,
            force3D: true
        });

        gridItems.forEach((item, i) => {
            gsap.set(item, { z: zValues[i], force3D: true });
        });

        // Timeline only handles animated properties
        const timeline = gsap.timeline({
            defaults: { ease: 'none' },
            scrollTrigger: {
                trigger: gridWrap,
                start: 'top bottom',
                end: 'bottom top',
                scrub: params.scrub,
                invalidateOnRefresh: false
            }
        });

        gridItems.forEach((item, i) => {
            timeline.fromTo(item, {
                xPercent: xFrom[i],
                yPercent: yFrom[i]
            }, {
                xPercent: xTo[i],
                yPercent: yTo[i],
                force3D: true
            }, 0);
        });
    };

    // Convert inline background-image to data-bg for lazy loading
    document.querySelectorAll('.grid__item-inner').forEach(el => {
        const style = el.style.backgroundImage;
        const match = style.match(/url\(['"]?(.+?)['"]?\)/);
        if (match) {
            el.dataset.bg = match[1];
            el.style.backgroundImage = '';
        }
    });

    lazyLoadImages().then(() => {
        applyGalleryAnimation();
    });
})();
