/*
 * Public problem statements for the dummy contest page.
 *
 * IMPORTANT: Only the *public* part of each problem lives here: the story,
 * the output format and the problem_id. The input shape and format
 * (TopologyService), the constraints (ConstraintService) and worked examples
 * (OracleService) are deliberately NOT published. Contestants must query the
 * four gRPC services (see ../project) with the problem_id to uncover them.
 */
window.PROBLEMS = [
  {
    id: 1,
    slug: "sum-it-up",
    title: "Sum It Up",
    difficulty: "Easy",
    maxScore: 10,
    successRate: "96.4%",
    statementHtml: `
      <p>Welcome to the webinar contest! This warm-up problem helps you get
      familiar with the investigation workflow before the main challenge.</p>
      <p>You are given a collection of integers. Your task is to compute their
      total.</p>
      <p>Before writing code, use <code>problem_id = 1</code> to query the
      investigation services. They will tell you everything this page does
      not.</p>
    `,
    outputFormat: `
      <p>Print a single integer — the total of all given values.</p>
    `,
  },
  {
    id: 2,
    slug: "hidden-delivery-route-challenge",
    title: "Hidden Delivery Route Challenge",
    difficulty: "Hard",
    maxScore: 90,
    successRate: "18.7%",
    statementHtml: `
      <p>A logistics company operates warehouses numbered <code>1</code> to
      <code>N</code>, linked by delivery routes. Every route has a delivery
      cost.</p>
      <p>The company also runs <em>promotional routes</em>, which change the
      effective delivery cost of a route.</p>
      <p>Find the <strong>cheapest total cost</strong> to deliver a package from
      <strong>Warehouse 1</strong> to <strong>Warehouse N</strong>.</p>
      <p>Choosing an algorithm is not about remembering its name. The decisive
      properties of the route network, the input layout and its limits are
      hidden. Use <code>problem_id = 2</code> to investigate with the gRPC
      services, form a hypothesis, test it with the oracle and validate your
      approach before you implement the final solution.</p>
    `,
    outputFormat: `
      <p>Print a single integer — the cheapest cost from Warehouse 1 to
      Warehouse N.</p>
      <p>If no valid delivery exists, print <code>UNREACHABLE</code>.</p>
    `,
  },
];
