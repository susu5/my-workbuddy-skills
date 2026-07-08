#!/usr/bin/env node
import fs from "node:fs";

const file = process.argv[2];
if (!file) {
  console.error("Usage: node validate-carousel-plan.mjs <plan.json>");
  process.exit(2);
}

const raw = fs.readFileSync(file, "utf8");
const plan = JSON.parse(raw);
const errors = [];

if (!Array.isArray(plan.pages) || plan.pages.length === 0) {
  errors.push("plan.pages must be a non-empty array");
}

for (const [index, page] of (plan.pages || []).entries()) {
  const prefix = `pages[${index}]`;
  for (const key of ["page_role", "title", "page_objective", "image_template_id"]) {
    if (!page[key]) errors.push(`${prefix}.${key} is required`);
  }
  if (page.body && Array.isArray(page.body) && page.body.length > 5) {
    errors.push(`${prefix}.body has more than 5 items; split the page or reduce text`);
  }
}

for (const key of ["dimension_id", "style_id"]) {
  if (!plan[key]) errors.push(`plan.${key} is required after user confirmation`);
}

if (plan.generated_full_set_before_sample_approval === true) {
  errors.push("full set cannot be generated before 3-sample approval");
}

if (errors.length) {
  console.error(errors.join("\n"));
  process.exit(1);
}

console.log("Carousel plan validation passed.");

