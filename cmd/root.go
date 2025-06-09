package cmd

import (
	"fmt"

	"github.com/morikuni/aec"
	"github.com/openfaas/faasd/pkg"
	"github.com/spf13/cobra"
)

// WelcomeMessage to introduce ofc-bootstrap
const WelcomeMessage = "Welcome to faasd"

func init() {
	rootCommand.AddCommand(versionCmd)
	rootCommand.AddCommand(upCmd)
	rootCommand.AddCommand(installCmd)
	rootCommand.AddCommand(makeProviderCmd())
	rootCommand.AddCommand(collectCmd)
	rootCommand.AddCommand(makeServiceCmd())
}

func RootCommand() *cobra.Command {
	return rootCommand
}

// Execute faasd
func Execute() error {
	fmt.Println("God is my Guiding Light")
	if err := rootCommand.Execute(); err != nil {
		return err
	}
	return nil
}

var rootCommand = &cobra.Command{
	Use:   "faasd",
	Short: "Start faasd",
	Long: `
faasd Community Edition (CE):

Learn how to build, secure, and monitor functions with faasd with 
the eBook:

https://openfaas.gumroad.com/l/serverless-for-everyone-else

License: OpenFaaS CE EULA with faasd addendum:

https://github.com/openfaas/faasd/blob/master/EULA.md
`,
	RunE:         runRootCommand,
	SilenceUsage: true,
}

func runRootCommand(cmd *cobra.Command, args []string) error {

	printLogo()
	cmd.Help()

	return nil
}

var versionCmd = &cobra.Command{
	Use:   "version",
	Short: "Display version information.",
	Run:   parseBaseCommand,
}

func parseBaseCommand(_ *cobra.Command, _ []string) {
	printLogo()

	printVersion()
}

func printVersion() {
	fmt.Printf("faasd Community Edition (CE) version: %s\tcommit: %s\n", pkg.GetVersion(), pkg.GitCommit)
}

func printLogo() {
	logoText := aec.WhiteF.Apply(Logo)
	fmt.Println(logoText)
}

// Logo for version and root command
const Logo = `  __                     _ 
 / _| __ _  __ _ ___  __| |
| |_ / _` + "`" + ` |/ _` + "`" + ` / __|/ _` + "`" + ` |
|  _| (_| | (_| \__ \ (_| |
|_|  \__,_|\__,_|___/\__,_|
`
