/**
 * @module faq.js
 * This module handles the interactive FAQ section. It toggles the visibility of FAQ answers
 * when a user clicks on a question.
 *
 */

// Select all FAQ items in the document
const faqItems = document.querySelectorAll(".faq-item");

/**
 * Adds click event listeners to each FAQ question element.
 * When a question is clicked, it toggles the 'active' class on its parent item,
 * typically used to show or hide the corresponding answer.
 */
faqItems.forEach((item) => {
  item.querySelector(".faq-question").addEventListener("click", () => {
    item.classList.toggle("active");
  });
});
