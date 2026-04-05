package config

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
)

const (
	// ConfigFile is the path to the workspace configuration file.
	ConfigFile = "instructions/.manifest/config.json"
	// RepoSubDir is the path where the skills repo is cloned into.
	RepoSubDir = "instructions"
)

// Config holds the persisted workspace configuration written by `skills init`.
type Config struct {
	RepoURL string   `json:"repo_url"`
	Groups  []string `json:"groups"`
	Skills  []string `json:"skills"`
}

// RepoPath returns the local filesystem path to the cloned skills repository.
func (c *Config) RepoPath() string {
	return RepoSubDir
}

// Load reads the workspace configuration from instructions/.manifest/config.json.
// Returns an actionable error if the file doesn't exist (workspace not initialized).
func Load() (*Config, error) {
	data, err := os.ReadFile(ConfigFile)
	if err != nil {
		if os.IsNotExist(err) {
			return nil, fmt.Errorf("not a skills workspace — run `skills init` first")
		}
		return nil, fmt.Errorf("failed to read config: %w", err)
	}

	var cfg Config
	if err := json.Unmarshal(data, &cfg); err != nil {
		return nil, fmt.Errorf("corrupted config (%s): %w", ConfigFile, err)
	}
	return &cfg, nil
}

// Save writes the configuration to instructions/.manifest/config.json, creating the directory if needed.
func Save(cfg *Config) error {
	if err := os.MkdirAll(filepath.Dir(ConfigFile), 0755); err != nil {
		return fmt.Errorf("failed to create instructions/.manifest/ directory: %w", err)
	}
	data, err := json.MarshalIndent(cfg, "", "  ")
	if err != nil {
		return err
	}
	return os.WriteFile(ConfigFile, data, 0644)
}
