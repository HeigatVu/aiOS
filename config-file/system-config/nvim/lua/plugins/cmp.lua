return {
  -- override nvim-cmp and add cmp-emoji
  {
    "hrsh7th/nvim-cmp",
    dependencies = {
      { "hrsh7th/cmp-emoji" },
    },
    opts = function(_, opts)
      table.insert(opts.sources, {
        { name = "emoji" },
        { name = "orgmode" },
      })
      local cmp = require("cmp")
      opts.window = {
        completion = cmp.config.window.bordered({}),
        documentation = cmp.config.window.bordered({}),
      }
      -- Set view to follow cursor while typing
      opts.view = {
        entries = {
          follow_cursor = true,
        },
      }
    end,
  },
}
