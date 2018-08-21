---
layout: post
title:  "About the Chart Object"
date:   2018-08-21 3:50:00 -0500
author: "Kimberly Orr"
categories: dev
tags: "about dev"
excerpt_separator: <!--read more-->
---

# About the Chart objects in mpl-altair

**ChartMetadata**

mplaltair starts the conversion by parsing the Altair chart and storing information about the chart as an object.

The `parse_chart.ChartMetatdata` object stores the chart's data, mark, and encodings. The encodings are each stored as `parse_chart.ChannelMetadata` objects.

**ChannelMetadata**

Each `parse_chart.ChannelMetadata` object parses and holds all of the necessary information for each encoding in an Altair chart. In this step, the specific data used for that encoding is stored as an array that Matplotlib can handle. Temporal data is converted to a Matplotlib-friendly format.