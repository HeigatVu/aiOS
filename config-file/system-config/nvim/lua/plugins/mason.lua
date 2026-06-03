return {
  {
    "mason.nvim",
    opts = function(_, opts)
      opts.ensure_installed = opts.ensure_installed or {}
      -- Remove go tools from automatic install since the container runtime is network-isolated
      local targets = { "gopls", "goimports", "gofumpt", "gomodifytags", "impl", "golangci-lint", "delve" }
      for _, target in ipairs(targets) do
        for i = #opts.ensure_installed, 1, -1 do
          if opts.ensure_installed[i] == target then
            table.remove(opts.ensure_installed, i)
          end
        end
      end
    end,
  },
  {
    "neovim/nvim-lspconfig",
    opts = {
      servers = {
        gopls = {
          mason = false, -- Prevent mason-lspconfig from trying to install gopls
        },
      },
    },
  },
}
