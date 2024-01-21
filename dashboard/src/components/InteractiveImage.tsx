import { useEffect } from 'react'

export const InteractiveImage = ({
  src,
  width,
  alt,
}: {
  src: any;
  width: number;
  alt: string;
}) => {
  useEffect(() => {
    const constrain = 500
    const mouseOverContainer = document.getElementById(`img-container-${src}`)
    const image = document.getElementById(`img-${src}`)
    function transforms (x: number, y: number, el: any) {
      const box = el.getBoundingClientRect()
      const calcX = -(y - box.y - box.height / 2) / constrain
      const calcY = (x - box.x - box.width / 2) / constrain

      return (
        'perspective(100px) ' +
        '   rotateX(' +
        calcX +
        'deg) ' +
        '   rotateY(' +
        calcY +
        'deg) '
      )
    }
    function transformElement (el: any, xyEl: any) {
      el.style.transform = transforms.apply(null, xyEl)
    }
    if (mouseOverContainer && image) {
      document.body.onmousemove = (e) => {
        const xy = [e.clientX, e.clientY]
        // @ts-ignore
        const position = xy.concat([image])
        window.requestAnimationFrame(function () {
          transformElement(image, position)
        })
      }
    }
  }, [src])
  return (
    <div id={`img-container-${src}`}>
      <img
        style={{ position: 'absolute' }}
        src={src}
        width={width}
        alt={alt}
        id={`img-${src}`}
      />
    </div>
  )
}
