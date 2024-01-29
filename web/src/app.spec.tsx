import { Admin } from "@/admin";
import { render, screen } from "@testing-library/react";

it("Test", () => {
  render(<Admin />);

  const button = screen.getByRole("button");
  expect(button).toBeEnabled();
});
