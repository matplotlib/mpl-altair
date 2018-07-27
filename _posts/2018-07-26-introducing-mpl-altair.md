---
layout: post
title:  "Why Matplotlib Altair?"
date:   2018-07-26 11:30:00 -0400
author: "Hannah Aizenman"
categories: about
tags: "intro about"
excerpt_separator: <!--read more-->
---

[Altair](https://altair-viz.github.io/) is a great library for building a range of interactive statistical visualizations, and offers a powerful and concise visualization grammar to do so. 

But, by design, the Altair API is limited:
>We realize that a declarative API will necessarily be limited
compared to the full programmatic APIs of Matplotlib, Bokeh, etc.
That is a deliberate design choice we feel is needed to simplify the
user experience of exploratory visualization.

This project aims to extend the full programmatic API of Matplotlib to Altair users by converting Altair chart objects to Matplotlib objects. This gives users the publication worthy graphics of Matplotlib, the ability to create iteractive dashboards composed of Altair & non-Altair charts, and the ability to customize their visualizations in any way Matplotlib supports (which is a lot of ways...)

Initial work on this project is supported by the [John Hunter Matplotlib Summer Fellowship](https://www.numfocus.org/blog/2018-john-hunter-matplotlib-summer-fellows), sponsored by [NumFocus](https://www.numfocus.org), in honor of the memory of Matplotlib creator John Hunter. This summer's fellows are Kimberly Orr and Nabarun Pal. 

This blog post is liberally inspired by Kimberley Orr's SciPy 2018 lightening
talk. 

