#version 440
layout(location = 0) in vec2 qt_TexCoord0;
layout(location = 0) out vec4 fragColor;

layout(std140, binding = 0) uniform buf {
    mat4 qt_Matrix;
    float qt_Opacity;
    vec4 tint;
    vec2 surfaceSize;
    float radius;
    float refraction;
    float aberration;
    float blurRadius;
};

layout(binding = 1) uniform sampler2D source;

float roundedBoxSDF(vec2 p, vec2 halfSize, float r) {
    vec2 q = abs(p) - halfSize + vec2(r);
    return length(max(q, 0.0)) + min(max(q.x, q.y), 0.0) - r;
}

vec3 blurAt(vec2 uv) {
    vec2 px = 1.0 / max(surfaceSize, vec2(1.0));
    vec2 d = px * blurRadius;
    vec3 c = texture(source, uv).rgb * 0.30;
    c += texture(source, uv + vec2( d.x, 0.0)).rgb * 0.175;
    c += texture(source, uv + vec2(-d.x, 0.0)).rgb * 0.175;
    c += texture(source, uv + vec2(0.0,  d.y)).rgb * 0.175;
    c += texture(source, uv + vec2(0.0, -d.y)).rgb * 0.175;
    return c;
}

void main() {
    vec2 size = max(surfaceSize, vec2(1.0));
    vec2 halfSize = size * 0.5;
    vec2 p = (qt_TexCoord0 - 0.5) * size;
    float sdf = roundedBoxSDF(p, halfSize, radius);
    float alpha = 1.0 - smoothstep(-1.0, 0.5, sdf);
    if (alpha <= 0.001) {
        fragColor = vec4(0.0);
        return;
    }

    float distIn = max(0.0, -sdf);
    float edgeWidth = 24.0;
    float edge = 1.0 - smoothstep(0.0, edgeWidth, distIn);

    float eps = 1.0;
    float dx = roundedBoxSDF(p + vec2(eps, 0.0), halfSize, radius)
             - roundedBoxSDF(p - vec2(eps, 0.0), halfSize, radius);
    float dy = roundedBoxSDF(p + vec2(0.0, eps), halfSize, radius)
             - roundedBoxSDF(p - vec2(0.0, eps), halfSize, radius);
    vec2 n = normalize(vec2(dx, dy) + vec2(1e-5));

    vec2 shift = -n * (refraction * edge) / size;
    float ca = aberration;
    vec3 bg;
    bg.r = blurAt(qt_TexCoord0 + shift * (1.0 + ca)).r;
    bg.g = blurAt(qt_TexCoord0 + shift).g;
    bg.b = blurAt(qt_TexCoord0 + shift * (1.0 - ca)).b;

    float tintA = clamp(tint.a, 0.0, 1.0);
    vec3 tintRgb = tintA > 0.001 ? tint.rgb / tintA : vec3(1.0);
    vec3 col = mix(bg, tintRgb, tintA);
    fragColor = vec4(col * alpha, alpha) * qt_Opacity;
}
