import { App } from "@/admin";
import { render, screen } from "@testing-library/react";

it("Test", () => {
  render(<App />);

  const button = screen.getByRole("button");
  expect(button).toBeEnabled();
});
