import React from "react";
import { Base } from "../base";
import BarChart from "./charts/bar-chart";
import Stack from "@mui/material/Stack";
import { CategoricalDatum } from "../types/data-types";

export const DualDistribution = ({
  data,
}: {
  data: { node: CategoricalDatum[]; granularity: any };
}) => {
  const node = data.node;
  const granularity = data.granularity;
  return (
    <Base>
      <Stack direction="row" spacing={2}>
        <BarChart data={node} />
        <BarChart data={granularity} />
      </Stack>
    </Base>
  );
};
