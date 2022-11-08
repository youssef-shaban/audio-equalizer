import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import React, { ReactNode } from "react"
import Slider, {
  SliderThumb,
  SliderValueLabelProps,
} from "@mui/material/Slider"
import { createTheme, styled } from "@mui/material/styles"
import Typography from "@mui/material/Typography"
import Tooltip from "@mui/material/Tooltip"
import Box from "@mui/material/Box"

const AirbnbSlider = styled(Slider)(({ theme }) => ({
  color: "#3a8589",
  margin: "30px 40px 0 40px",
  padding: "0px 13px",
  "& .MuiSlider-thumb": {
    width: 27,
    height: 27,
    backgroundColor: "#fff",
    border: "1px solid currentColor",
    "&:hover": {
      boxShadow: "0 0 0 8px rgba(58, 133, 137, 0.16)",
    },
    "& .airbnb-bar": {
      height: 9,
      width: 1,
      backgroundColor: "currentColor",
      marginLeft: 1,
      marginRight: 1,
    },
  },
  "& .MuiSlider-track": {
    width: 6,
  },
  "& .MuiSlider-rail": {
    color: theme.palette.mode === "dark" ? "#bfbfbf" : "#d8d8d8",
    opacity: theme.palette.mode === "dark" ? undefined : 1,
    width: 4,
  },
  "& .MuiSlider-valueLabel": {
    fontSize: 12,
    width: 30,
    background: "unset",
    borderRadius: "22%",
    backgroundColor: "#3a8589",
  },
}))

interface AirbnbThumbComponentProps extends React.HTMLAttributes<unknown> {}

function AirbnbThumbComponent(Props: AirbnbThumbComponentProps) {
  const { children, ...other } = Props

  return (
    <SliderThumb {...other}>
      {children}
      <span className="airbnb-bar" />
      <span className="airbnb-bar" />
      <span className="airbnb-bar" />
    </SliderThumb>
  )
}

class VetricalSlider extends StreamlitComponentBase {
  public render = (): ReactNode => {
    const maxV = this.props.args["maxValue"]
    const minV = this.props.args["minValue"]
    const defaultV = this.props.args["default"]
    const step = this.props.args["step"]
    const label = this.props.args["label"]
    const height = this.props.args["height"]

    return (
      <Box sx={{ height: height }}>
        <AirbnbSlider
          sx={{
            '& input[type="range"]': {
              WebkitAppearance: "slider-vertical",
            },
          }}
          orientation="vertical"
          slots={{ thumb: AirbnbThumbComponent }}
          defaultValue={defaultV}
          max={maxV}
          min={minV}
          step={step}
          valueLabelDisplay="auto"
          onChangeCommitted={(event, value) => {
            Streamlit.setComponentValue(Number(value))
          }}
          disabled={this.props.args["disabled"]}
        />
        <Box ml={4}>
          <Typography>{label}</Typography>
        </Box>
      </Box>
    )
  }
}

export default withStreamlitConnection(VetricalSlider)
