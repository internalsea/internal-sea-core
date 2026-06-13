export function AppWaveBackground() {
  return (
    <div aria-hidden="true" className="pointer-events-none absolute inset-0 overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_90%_70%_at_50%_-10%,rgb(168_189_209_/_0.35),transparent_55%)]" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_70%_50%_at_100%_40%,rgb(148_175_199_/_0.22),transparent_50%)]" />
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_60%_45%_at_0%_70%,rgb(176_196_214_/_0.2),transparent_45%)]" />

      <svg
        className="absolute bottom-0 left-0 h-[42%] w-full text-auth-wave opacity-[0.18]"
        preserveAspectRatio="none"
        viewBox="0 0 1440 400"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M0,220 C240,320 480,120 720,220 C960,320 1200,140 1440,240 L1440,400 L0,400 Z"
          fill="currentColor"
        />
      </svg>

      <svg
        className="absolute bottom-0 left-0 h-[34%] w-full text-auth-wave opacity-[0.28]"
        preserveAspectRatio="none"
        viewBox="0 0 1440 400"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M0,260 C320,160 560,300 840,240 C1080,190 1260,280 1440,220 L1440,400 L0,400 Z"
          fill="currentColor"
        />
      </svg>

      <svg
        className="absolute bottom-0 left-0 h-[26%] w-full text-auth-wave opacity-[0.14]"
        preserveAspectRatio="none"
        viewBox="0 0 1440 400"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M0,300 C200,240 400,340 640,280 C880,220 1120,320 1440,260 L1440,400 L0,400 Z"
          fill="currentColor"
        />
      </svg>
    </div>
  )
}
